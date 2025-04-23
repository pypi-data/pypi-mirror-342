import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
import json
import textwrap
import asyncio
import requests
import ast
import rich
from rich.tree import Tree
from .models import (
    VSCodeConfigFile,
    VSCodeMCPConfig,
    ClaudeConfigFile,
    SSEServer,
    StdioServer,
)
from .suppressIO import SuppressStd
from collections import namedtuple
from datetime import datetime
from hashlib import md5
import pyjson5
from lark import Lark

Result = namedtuple("Result", field_names=["value", "message"], defaults=[None, None])

def rebalance_command_args(command, args):
    # create a parser that splits on whitespace,
    # unless it is inside "." or '.'
    # unless that is escaped
    parser = Lark(r'''
        command: (PART|SQUOTEDPART|DQUOTEDPART)*
        PART: /[^\s'".]+/
        SQUOTEDPART: /'[^']'/
        DQUOTEDPART: /"[^"]"/
        ''',
        parser="lalr",
        lexer="standard",
        start="command",
        regex=True,
    )
    tree = parser.parse(command)
    command = [node.value for node in tree.children]
    args = (args or []) + command[1:]
    command = command[0]
    return command, args

def format_err_str(e, max_length=None):
    try:
        if isinstance(e, ExceptionGroup):
            text = ", ".join([format_err_str(e) for e in e.exceptions])
        elif isinstance(e, TimeoutError):
            text = "Could not reach server within timeout"
        else:
            raise Exception()
    except:
        text = None
    if text is None:
        name = type(e).__name__
        try:

            def _mapper(e):
                if isinstance(e, Exception):
                    return format_err_str(e)
                return str(e)

            message = ",".join(map(_mapper, e.args))
        except Exception:
            message = str(e)
        message = message.strip()
        if len(message) > 0:
            text = f"{name}: {message}"
        else:
            text = name
    if max_length is not None and len(text) > max_length:
        text = text[: (max_length - 3)] + "..."
    return text


def format_path_line(path, status, operation="Scanning"):
    text = f"● {operation} [bold]{path}[/bold] [gray62]{status}[/gray62]"
    return rich.text.Text.from_markup(text)


def format_servers_line(server, status=None):
    text = f"[bold]{server}[/bold]"
    if status:
        text += f" [gray62]{status}[/gray62]"
    return rich.text.Text.from_markup(text)


def format_tool_line(
    tool,
    verified: Result,
    changed: Result = Result(),
    type="tool",
    include_description=False,
    additional_text=None,
):
    is_verified = verified.value
    if is_verified is not None and changed.value is not None:
        is_verified = is_verified and not changed.value

    message = [verified.message, changed.message]
    message = [m for m in message if m is not None]
    message = ", ".join(message)

    color = {True: "[green]", False: "[red]", None: "[gray62]"}[is_verified]
    icon = {True: ":white_heavy_check_mark:", False: ":cross_mark:", None: ""}[
        is_verified
    ]
    name = tool.name
    if len(name) > 25:
        name = name[:22] + "..."
    name = name + " " * (25 - len(name))
    text = f"{type} {color}[bold]{name}[/bold] {icon} {message}"

    if include_description:
        if hasattr(tool, "description"):
            description = tool.description
        else:
            description = "<no description available>"
        text += f"\n[gray62][bold]Current description:[/bold]\n{description}[/gray62]"

    if additional_text is not None:
        text += f"\n[gray62]{additional_text}[/gray62]"

    text = rich.text.Text.from_markup(text)
    return text


def format_inspect_tool_line(
    tool,
):
    name = tool.name
    if len(name) > 25:
        name = name[:22] + "..."
    name = name + " " * (25 - len(name))

    if hasattr(tool, "description"):
        # dedent the description
        description = tool.description
        # wrap the description to 80 characters
        description = textwrap.dedent(description)
    else:
        description = "<no description available>"

    color = "[gray62]"
    icon = ""
    type = "tool"
    message = ""
    text = f"{type} {color}[bold]{name}[/bold] {icon} {message}"
    text += f"\n{description}"

    text = rich.text.Text.from_markup(text)
    return text

def upload_whitelist_entry(name, hash, base_url):
    url = base_url + "/api/v1/public/mcp-whitelist"
    headers = {"Content-Type": "application/json"}
    data = {
        "name": name,
        "hash": hash,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))

def verify_server(tools, prompts, resources, base_url):
    if len(tools) == 0:
        return []
    messages = [
        {
            "role": "system",
            "content": f"Tool Name:{tool.name}\nTool Description:{tool.description}",
        }
        for tool in tools
    ]
    url = base_url + "/api/v1/public/mcp"
    headers = {"Content-Type": "application/json"}
    data = {
        "messages": messages,
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response = response.json()
            results = [Result(True, "verified") for _ in tools]
            for error in response["errors"]:
                key = ast.literal_eval(error["key"])
                idx = key[1][0]
                results[idx] = Result(False, "failed - " + " ".join(error["args"]))
            return results
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        try:
            errstr = str(e.args[0])
            errstr = errstr.splitlines()[0]
        except Exception:
            errstr = ""
        return [
            Result(None, "could not reach verification server " + errstr) for _ in tools
        ]


async def check_server(
    server_config: SSEServer | StdioServer, timeout, suppress_mcpserver_io
):
    is_sse = isinstance(server_config, SSEServer)

    def get_client(server_config):
        if is_sse:
            return sse_client(
                url=server_config.url,
                headers=server_config.headers,
                # env=server_config.env, #Not supported by MCP yet, but present in vscode
                timeout=timeout,
            )
        else:
            # handle complex configs
            command, args = rebalance_command_args(server_config.command, server_config.args)
            server_params = StdioServerParameters(
                command=command,
                args=args,
                env=server_config.env,
            )
            return stdio_client(server_params)

    async def _check_server():
        async with get_client(server_config) as (read, write):
            async with ClientSession(read, write) as session:
                meta = await session.initialize()
                # for see servers we need to check the announced capabilities
                if not is_sse or meta.capabilities.prompts.supported:
                    try:
                        prompts = await session.list_prompts()
                        prompts = list(prompts.prompts)
                    except:
                        prompts = []
                else:
                    prompts = []
                if not is_sse or meta.capabilities.resources.supported:
                    try:
                        resources = await session.list_resources()
                        resources = list(resources.resources)
                    except:
                        resources = []
                else:
                    resources = []
                if not is_sse or meta.capabilities.tools.supported:
                    try:
                        tools = await session.list_tools()
                        tools = list(tools.tools)
                    except:
                        tools = []
                else:
                    tools = []
                return prompts, resources, tools

    if suppress_mcpserver_io:
        with SuppressStd():
            return await _check_server()
    else:
        return await _check_server()


async def check_server_with_timeout(server_config, timeout, suppress_mcpserver_io):
    return await asyncio.wait_for(
        check_server(server_config, timeout, suppress_mcpserver_io), timeout
    )


def scan_config_file(path):
    path = os.path.expanduser(path)

    def parse_and_validate(config):
        models = [
            ClaudeConfigFile,  # used by most clients
            VSCodeConfigFile,  # used by vscode settings.json
            VSCodeMCPConfig,  # used by vscode mcp.json
        ]
        errors = []
        for model in models:
            try:
                return model.parse_obj(config)
            except Exception as e:
                errors.append(e)
        if len(errors) > 0:
            raise Exception(
                "Could not parse config file as any of "
                + str([model.__name__ for model in models])
                + "\nErrors:\n"
                + "\n".join([str(e) for e in errors])
            )
        raise Exception("Could not parse config file")

    with open(path, "r") as f:
        # use json5 to support comments as in vscode
        config = pyjson5.load(f)
        # try to parse model
        model = parse_and_validate(config)
        if isinstance(model, VSCodeConfigFile):
            servers = model.mcp.servers
        elif isinstance(model, VSCodeMCPConfig):
            servers = model.servers
        elif isinstance(model, ClaudeConfigFile):
            servers = model.mcpServers
        else:
            assert False
        return servers


class StorageFile:
    def __init__(self, path):
        self.path = path
        self.data = {}
        if os.path.exists(path):
            with open(path, "r") as f:
                self.data = json.load(f)
    
    @property
    def whitelist(self):
        return self.data.get("__whitelist", {})

    def reset_whitelist(self):
        self.data["__whitelist"] = {}
        
    def compute_hash(self, tool):
        return md5(tool.description.encode()).hexdigest()

    def check_and_update(self, server_name, tool, verified):
        key = f"{server_name}.{tool.name}"
        hash = self.compute_hash(tool)
        new_data = {
            "hash": hash,
            "timestamp": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            "description": tool.description,
        }
        changed = False
        message = None
        prev_data = None
        if key in self.data:
            prev_data = self.data[key]
            changed = prev_data["hash"] != new_data["hash"]
            if changed:
                message = (
                    "tool description changed since previous scan at "
                    + prev_data["timestamp"]
                )
        self.data[key] = new_data
        return Result(changed, message), prev_data

    def print_whitelist(self):
        whitelist_keys = sorted(self.whitelist.keys())
        for key in whitelist_keys:
            rich.print(key, self.whitelist[key])
        rich.print(f"[bold]{len(whitelist_keys)} entries in whitelist[/bold]")

    def add_to_whitelist(self, name, hash):
        self.data["__whitelist"][name] = hash
        self.save()

    def is_whitelisted(self, tool):
        hash = self.compute_hash(tool)
        return hash in self.whitelist.values()

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f)


class MCPScanner:
    def __init__(
        self,
        files=[],
        base_url="https://mcp.invariantlabs.ai/",
        checks_per_server=1,
        storage_file="~/.mcp-scan",
        server_timeout=10,
        suppress_mcpserver_io=True,
        **kwargs,
    ):
        self.paths = files
        self.base_url = base_url
        self.checks_per_server = checks_per_server
        self.storage_file_path = os.path.expanduser(storage_file)
        self.storage_file = StorageFile(self.storage_file_path)
        self.server_timeout = server_timeout
        self.suppress_mcpserver_io = suppress_mcpserver_io

    def inspect_path(self, path, verbose=True):
        """
        Just inspects the server and prints the tools, prompts and resources without checking them.
        """
        status = "unknown"
        try:
            servers = scan_config_file(path)
            status = f"found {len(servers)} server{'' if len(servers) == 1 else 's'}"
        except FileNotFoundError:
            status = "file does not exist"
            return
        except json.JSONDecodeError:
            status = "invalid json"
            return
        except Exception:
            status = "failed to parse"
            return
        finally:
            if verbose:
                rich.print(format_path_line(path, status, operation="Inspecting"))

        path_print_tree = Tree("│")
        for server_name, server_config in servers.items():
            try:
                prompts, resources, tools = asyncio.run(
                    check_server_with_timeout(
                        server_config, self.server_timeout, self.suppress_mcpserver_io
                    )
                )
                status = None
            except TimeoutError as e:
                status = "Could not reach server within timeout"
                continue
            except Exception as e:
                status = str(e).splitlines()[0] + "..."
                continue
            finally:
                server_print = path_print_tree.add(
                    format_servers_line(server_name, status)
                )

            for tool in tools:
                server_print.add(format_inspect_tool_line(tool))

            for prompt in prompts:
                server_print.add(format_inspect_tool_line(prompt))

            for resource in resources:
                server_print.add(format_inspect_tool_line(resource))

        if len(servers) > 0 and verbose:
            rich.print(path_print_tree)

    def scan(self, path, verbose=True):
        try:
            servers = scan_config_file(path)
            status = f"found {len(servers)} server{'' if len(servers) == 1 else 's'}"
        except FileNotFoundError:
            status = f"file does not exist"
            return
        except Exception:
            status = f"could not parse file"
            return
        finally:
            if verbose:
                rich.print(format_path_line(path, status))

        path_print_tree = Tree("│")
        servers_with_tools = {}
        for server_name, server_config in servers.items():
            try:
                prompts, resources, tools = asyncio.run(
                    check_server_with_timeout(
                        server_config, self.server_timeout, self.suppress_mcpserver_io
                    )
                )
                status = None
            except Exception as e:
                status = format_err_str(e)
                continue
            finally:
                server_print = path_print_tree.add(
                    format_servers_line(server_name, status)
                )
            servers_with_tools[server_name] = tools

            verification_result = verify_server(
                tools, prompts, resources, base_url=self.base_url
            )
            for tool, verified in zip(tools, verification_result):
                changed, prev_data = self.storage_file.check_and_update(
                    server_name, tool, verified.value
                )
                additional_text = None
                if changed.value is True:
                    additional_text = f"[bold]Previous description({prev_data['timestamp']}):[/bold]\n{prev_data['description']}"
                if self.storage_file.is_whitelisted(tool):
                    verified = Result(
                        True,
                        message="[bold]tool whitelisted[/bold] " + verified.message,
                    )
                elif verified.value is False or changed.value is True:
                    hash = self.storage_file.compute_hash(tool)
                    message = f'[bold]You can whitelist this tool by running `mcp-scan whitelist "{tool.name}" {hash}`[/bold]'
                    if additional_text is not None:
                        additional_text += '\n\n' + message
                    else:
                        additional_text = message
                server_print.add(
                    format_tool_line(
                        tool,
                        verified,
                        changed,
                        include_description=(
                            verified.value is False or changed.value is True
                        ),
                        additional_text=additional_text,
                    )
                )
            for prompt in prompts:
                server_print.add(
                    format_tool_line(prompt, Result(message="skipped"), type="prompt")
                )
            for resource in resources:
                server_print.add(
                    format_tool_line(
                        resource, Result(message="skipped"), type="resource"
                    )
                )

        if len(servers) > 0 and verbose:
            rich.print(path_print_tree)

        # cross-references check
        # for each tool check if it referenced by tools of other servers
        cross_ref_found = False
        cross_reference_sources = set()
        for server_name, tools in servers_with_tools.items():
            other_server_names = set(servers.keys())
            other_server_names.remove(server_name)
            other_tool_names = [
                tool.name
                for s in other_server_names
                for tool in servers_with_tools.get(s, [])
            ]
            flagged_names = list(other_server_names) + other_tool_names
            flagged_names = set(map(str.lower, flagged_names))
            for tool in tools:
                tokens = tool.description.lower().split()
                for token in tokens:
                    if token in flagged_names:
                        cross_ref_found = True
                        cross_reference_sources.add(token)
        if verbose:
            if cross_ref_found:
                rich.print(
                    rich.text.Text.from_markup(
                        f"\n[bold yellow]:construction: Cross-Origin Violation: Tool descriptions of server {cross_reference_sources} explicitly mention tools of other servers, or other servers.[/bold yellow]"
                    ),
                )
            rich.print()

    def reset_whitelist(self):
        self.storage_file.reset_whitelist()
        self.storage_file.save()
        rich.print("Whitelist reset")

    def print_whitelist(self):
        self.storage_file.print_whitelist()

    def whitelist(self, name, hash, local_only=False):
        self.storage_file.add_to_whitelist(name, hash)
        self.storage_file.save()
        if not local_only:
            upload_whitelist_entry(
                name, hash, self.base_url
            )

    def start(self):
        for i, path in enumerate(self.paths):
            for k in range(self.checks_per_server):
                self.scan(path, verbose=(k == self.checks_per_server - 1))
            if i < len(self.paths) - 1:
                rich.print("")
        self.storage_file.save()

    def inspect(self):
        for i, path in enumerate(self.paths):
            self.inspect_path(path, verbose=True)
            if i < len(self.paths) - 1:
                rich.print("")
        self.storage_file.save()

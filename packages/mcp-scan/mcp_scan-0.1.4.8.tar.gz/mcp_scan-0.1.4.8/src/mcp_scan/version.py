from importlib.metadata import version, PackageNotFoundError

try:
    version_info = version("mcp-scan")
except PackageNotFoundError:
    version_info = "unknown"

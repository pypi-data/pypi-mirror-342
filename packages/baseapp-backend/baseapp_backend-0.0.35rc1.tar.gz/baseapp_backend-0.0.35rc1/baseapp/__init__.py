from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("package-name")
except PackageNotFoundError:
    __version__ = None

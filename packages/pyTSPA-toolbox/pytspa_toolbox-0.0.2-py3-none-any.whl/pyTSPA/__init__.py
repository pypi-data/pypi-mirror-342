from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("pyTSPA_toolbox")
except PackageNotFoundError:
    __version__ = "0.0.2"
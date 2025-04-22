from dqrobotics_extensions.pyplot._pyplot import plot

# https://setuptools-git-versioning.readthedocs.io/en/stable/runtime_version.html
from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("dqrobotics-pyplot")
except PackageNotFoundError:
    # package is not installed
    pass
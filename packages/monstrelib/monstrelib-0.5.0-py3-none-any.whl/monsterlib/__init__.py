from .core import add, subtract  # noqa: F401

try:
    from setuptools_scm import get_version

    __version__ = get_version(root="..", relative_to=__file__)
except ImportError:
    __version__ = "0.0.0"  # fallback pour les environnements sans Git

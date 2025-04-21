"""proxy [`Module`].

Contains high grade tools for converting any given module into a
restricted proxy.
"""

import types

class ProxyGenerator:
    """A native proxy generator for modules that generates and sets a
    restricted proxy of the concerned module. The generated proxy acts
    as the concerned module and restricts user access to any private
    code.

    Must be the last line of code for the concerned module.
    """

    @staticmethod
    def generateFor_(module: types.ModuleType, *public: str) -> types.ModuleType:
        """The most basic functionality the `ProxyGenerator` class offers; Creates
        and returns the proxy module from any given module."""

    @staticmethod
    def automaticSetup_(__name__: str, *public: str, NameToCheck: str = ...) -> None:
        """Automatically sets the proxy for any given module without the requirement of explicit
        `__name__` check and implementation."""
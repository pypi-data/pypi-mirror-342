"""localhost [`Module`].

Contains all preparation stage setups
"""

from typing import TypedDict

class _Location(TypedDict):
    latitude: float
    longitude: float
    accuracy: float
    address: str



def captureLocation_(timeout: float = ...) -> _Location: ...
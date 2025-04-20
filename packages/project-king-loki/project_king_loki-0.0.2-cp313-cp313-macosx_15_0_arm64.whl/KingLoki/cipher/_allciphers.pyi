
from KingLoki.cipher._format import Compressed, Encrypted
from typing import TypeVar, Generic

T = TypeVar('T')
E = TypeVar('E')
D = TypeVar('D')


class MemoryHardCipher_Sc(Generic[E, D]):

    def __init__(self, enable_encryption: E, enable_decryption: D) -> None: ...

    def encrypt_(self, content: T, password: Compressed[bytes] = ..., salt: Compressed[bytes] = ..., /) -> Encrypted[T]: ...
    def decrypt_(self, encrypted: Encrypted[T], password: Compressed[bytes] = ..., /) -> T: ...


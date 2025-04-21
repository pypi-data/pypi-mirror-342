
from KingLoki.cipher import Encrypted
from os import PathLike
from io import BufferedReader, BufferedWriter

class Loki:
    """The `Loki Protocol` for encryption!
    
    Inspired by the norse god of mischief and ofcource the god of stories (at
    later stages), this encryption protocol uses geocode for encryption making
    sure, decryption is only possible at a specific location. If security is
    what you care for most, this protocol is your ideal choice among others.

    The `Loki Protocol` encrypts in 5 undisclosed stages based on your system's
    geocode, which will be collected with your consent through the default
    system browser.

    Decryption failure at any particular stage will result in complete failure.

    Usage:
    ```python
    # initial setup
    Loki.setupPreRequisitesForProtocol_(wcount=10) # default worker count is 5.

    # encryption/decryption
    assert [1, 2, 3] == Loki.decryptionProtocolFromContentToContent_(
                    Loki.encryptionProtocolFromContentToContent_(
                    [1, 2, 3]))

    # end
    Loki.finalize()
    ```

    While using this with the `with` keyword, to increase the worker count, use:

    ```python
    Loki.set_worker_count(workers=10) # before using the with statement

    with Loki as loki:
        loki.encryptionProtocolFromContentToFile_(...)

    ```
    """

    workers: int

    @classmethod
    def setupPreRequisitesForProtocol_(cls, wcount: int = ...) -> None:
        """Sets all required protocol variables before proceeding further.
        This method needs to be called the first thing before proceeding to
        using any protocol variant.

        The `wcount` parameter represents the number of slaves to create. Defaults
        to 5 and only accepts an integer greater than or equal to 5.
        """

    @classmethod
    def encryptionProtocolFromContentToContent_(cls, content) -> Encrypted[bytes]:
        """Encrypts any given python object and returns another object"""

    @classmethod
    def decryptionProtocolFromContentToContent_(cls, encrypted: Encrypted[bytes]) -> object:
        """Decrypts encrypted object back to original object."""

    @classmethod
    def encryptionProtocolFromFileToFile(
            cls,
            sourceFilePath: PathLike = ...,
            sourceFileReader: BufferedReader = ...,
            autoCloseReader=True,
            destinationFilePath: PathLike = ...,
            destinationFileWriter: BufferedWriter = ...,
            autoCloseWriter=True
    ) -> None:
        """Encrypts any given source file and writes encrypted contents into given
        destination. Atleast one of the source and destination parameters needs to be
        present."""


    @classmethod
    def decryptionProtocolFromFileToFile_(
            cls,
            sourceFilePath: PathLike = ...,
            sourceFileReader: BufferedReader = ...,
            autoCloseReader=True,
            destinationFilePath: PathLike = ...,
            destinationFileWriter: BufferedWriter = ...,
            autoCloseWriter=True
    ) -> None:
        """Decrypts any encrypted file and writes decrypted contents into given
        destination. Atleast one of the source and destination parameters needs to be
        present.The original object must be bytes else this protocol variant will raise
        RuntimeError."""


    @classmethod
    def encryptionProtocolFromFileToContent_(
            cls,
            sourceFilePath: PathLike = ...,
            sourceFileReader: BufferedReader = ...,
            autoCloseReader=True
    ) -> Encrypted[bytes]:
        """Encrypts content from any given source file and returns the encrypted contents
        as a python object. Any one of the source parameters must be present."""


    @classmethod
    def decryptionProtocolFromFileToContent_(
            cls,
            sourceFilePath: PathLike = ...,
            sourceFileReader: BufferedReader = ...,
            autoCloseReader=True
    ) -> object:
        """Decryptes any encrypted file source and returns the decrypted object.
        Any one of the source parameters must be present."""

    @classmethod
    def encryptionProtocolFromContentToFile_(
            cls,
            content,
            destinationFilePath: PathLike = ...,
            destinationFileWriter: BufferedWriter = ...,
            autoCloseWriter=True
    ) -> None:
        """Encrypts any given python object and writes it to given destination file. Any one
        of the destination parameters must be present."""

    @classmethod
    def decryptionProtocolFromContentToFile_(
            encrypted: Encrypted[bytes],
            destinationFilePath: PathLike = ...,
            destinationFileWriter: BufferedWriter = ...,
            autoCloseWriter=True
    ) -> None:
        """Decrypts any given encrypted object and writes it to given destination file. Any one
        of the destination parameters must be present. The original object must be bytes else
        this protocol variant will raise RuntimeError."""

    @classmethod
    def finalize(cls) -> None:
        """Finalizes the `Loki Protocol` back to the state before `setupPreRequisitesForProtocol_`
        was called."""

    @classmethod
    def set_worker_count(cls, workers=5) -> None:
        """Sets the slave count for `Loki Protocol`. This method must be called before using `with`
        keyword on `Loki` class, if worker thread count needs to be increased. Only accepts a number
        ≥ 5."""

    @classmethod
    def __enter__(cls) -> 'Loki': ...
    @classmethod
    def __exit__(cls, *args, **kwargs): ...
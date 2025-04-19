class ZMPrinterError(Exception):
    """Base exception class for all zmprinter SDK errors."""

    def __init__(self, message, original_exception=None):
        super().__init__(message)
        self.original_exception = original_exception


class ZMPrinterSetupError(ZMPrinterError):
    """Error during SDK initialization or setup."""

    pass


class ZMPrinterImportError(ZMPrinterSetupError):
    """Failed to load or import LabelPrinter.dll or its .NET dependencies."""

    pass


class ZMPrinterDependencyError(ZMPrinterSetupError):
    """Required dependencies (like .NET Runtime) might be missing."""

    pass  # This might be hard to detect directly, often manifests as ImportError


class ZMPrinterConfigError(ZMPrinterError):
    """Invalid configuration or input data provided to the SDK."""

    pass


class ZMPrinterInvalidElementError(ZMPrinterConfigError):
    """Error creating or validating a LabelElement."""

    def __init__(self, message, element_name=None, original_exception=None):
        super().__init__(message, original_exception)
        self.element_name = element_name


class ZMPrinterCommunicationError(ZMPrinterError):
    """Error communicating with the printer (USB, Network)."""

    pass


class ZMPrinterConnectionTimeoutError(ZMPrinterCommunicationError):
    """Communication with the printer timed out."""

    pass


class ZMPrinterUSBError(ZMPrinterCommunicationError):
    """Specific error related to USB communication."""

    # Status codes -101, -102, -103, -104 could potentially raise this
    pass


class ZMPrinterNetworkError(ZMPrinterCommunicationError):
    """Specific error related to Network communication."""

    pass


class ZMPrinterStateError(ZMPrinterError):
    """Error related to the printer's hardware state (paper out, cover open, etc.)."""

    def __init__(self, message, status_code=None, status_message=None, original_exception=None):
        full_message = (
            f"{message} (Status Code: {status_code}, Info: {status_message})" if status_code is not None else message
        )
        super().__init__(full_message, original_exception)
        self.status_code = status_code
        self.status_message = status_message  # The descriptive message


class ZMPrinterCommandError(ZMPrinterError):
    """Error reported by the underlying LabelPrinter.dll when executing a command."""

    def __init__(self, message, dll_message=None, original_exception=None):
        full_message = f"{message}: {dll_message}" if dll_message else message
        super().__init__(full_message, original_exception)
        self.dll_message = dll_message  # The raw error from the DLL


class ZMPrinterLSFError(ZMPrinterError):
    """Error related to loading, parsing, or processing LSF label files."""

    pass


class ZMPrinterRFIDError(ZMPrinterError):
    """Base class for errors during RFID operations."""

    pass


class ZMPrinterRFIDReadError(ZMPrinterRFIDError):
    """Error while attempting to read an RFID tag."""

    def __init__(self, message, dll_message=None, original_exception=None):
        full_message = f"{message}: {dll_message}" if dll_message else message
        super().__init__(full_message, original_exception)
        self.dll_message = dll_message  # The raw error from the DLL


class ZMPrinterRFIDWriteError(ZMPrinterRFIDError):
    """Error while attempting to write to an RFID tag (usually during print)."""

    # Often detected via ZMPrinterCommandError from print_label
    pass


class ZMPrinterRFIDTagNotFoundError(ZMPrinterRFIDError):
    """RFID tag was not detected within range or timeout."""

    pass  # Could be raised if DLL indicates tag not found explicitly


class ZMPrinterRFIDTimeoutError(ZMPrinterRFIDError, ZMPrinterConnectionTimeoutError):
    """RFID operation timed out."""

    pass  # Inherits from both for flexibility


class ZMPrinterDataError(ZMPrinterError):
    """Error during internal data conversion or processing (e.g., image conversion)."""

    pass

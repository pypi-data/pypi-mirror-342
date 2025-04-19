# zmprinter_sdk/__init__.py
from .core import LabelPrinterSDK
from .config import PrinterConfig, LabelConfig
from .elements import (
    LabelElement,
    TextElement,
    BarcodeElement,
    ImageElement,
    RFIDElement,
    ShapeElement,
    LabelElementType,
)
from .enums import (
    PrinterStyle,
    BarcodeType,
    RFIDEncoderType,
    RFIDDataBlock,
    RFIDDataType,
)
from .utils import get_logger, setup_file_logging
from .exceptions import (
    ZMPrinterError,
    ZMPrinterSetupError,
    ZMPrinterImportError,
    ZMPrinterDependencyError,
    ZMPrinterConfigError,
    ZMPrinterInvalidElementError,
    ZMPrinterCommunicationError,
    ZMPrinterConnectionTimeoutError,
    ZMPrinterUSBError,
    ZMPrinterNetworkError,
    ZMPrinterStateError,
    ZMPrinterCommandError,
    ZMPrinterLSFError,
    ZMPrinterRFIDError,
    ZMPrinterRFIDReadError,
    ZMPrinterRFIDWriteError,
    ZMPrinterRFIDTagNotFoundError,
    ZMPrinterRFIDTimeoutError,
    ZMPrinterDataError,
)

# 设置包级别的 logger
logger = get_logger("zmprinter")

# Optional: Define __all__ for explicit export control
__all__ = [
    "LabelPrinterSDK",
    "PrinterConfig",
    "LabelConfig",
    "LabelElement",
    "TextElement",
    "BarcodeElement",
    "ImageElement",
    "RFIDElement",
    "ShapeElement",
    "LabelElementType",
    "PrinterStyle",
    "BarcodeType",
    "RFIDEncoderType",
    "RFIDDataBlock",
    "RFIDDataType",
    "get_logger",
    "setup_file_logging",
    "logger",
    "ZMPrinterError",
    "ZMPrinterSetupError",
    "ZMPrinterImportError",
    "ZMPrinterDependencyError",
    "ZMPrinterConfigError",
    "ZMPrinterInvalidElementError",
    "ZMPrinterCommunicationError",
    "ZMPrinterConnectionTimeoutError",
    "ZMPrinterUSBError",
    "ZMPrinterNetworkError",
    "ZMPrinterStateError",
    "ZMPrinterCommandError",
    "ZMPrinterLSFError",
    "ZMPrinterRFIDError",
    "ZMPrinterRFIDReadError",
    "ZMPrinterRFIDWriteError",
    "ZMPrinterRFIDTagNotFoundError",
    "ZMPrinterRFIDTimeoutError",
    "ZMPrinterDataError",
]

__version__ = "0.1.5"

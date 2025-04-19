from enum import Enum


class PrinterStyle(Enum):
    """打印机接口类型枚举 (对应 C# LabelPrinter.PrinterStyle)"""

    DRIVER = 0  # 通过驱动程序打印普通标签
    USB = 1  # (推荐)通过USB端口打印普通标签（无需驱动）
    NET = 2  # 通过网络IP打印普通标签（无需驱动）
    RFID_DRIVER = 3  # 通过驱动程序打印RFID标签
    RFID_USB = 4  # (推荐)通过USB端口打印RFID标签（无需驱动）
    RFID_NET = 5  # 通过网络IP打印RFID标签（无需驱动）
    GBGM_USB = 6  # RFID国标国密通过USB端口打印RFID标签（无需驱动）
    GBGM_NET = 7  # RFID国标国密通过网络IP打印RFID标签（无需驱动）
    GJB_USB = 8  # RFID国军标通过USB端口打印RFID标签（无需驱动）
    GJB_NET = 9  # RFID国军标通过网络IP打印RFID标签（无需驱动）


class BarcodeType(Enum):
    """常用条码类型"""

    CODE_128_AUTO = "Code 128 Auto"
    CODE_128_A = "Code 128 A"
    CODE_128_B = "Code 128 B"
    CODE_128_C = "Code 128 C"
    EAN_13 = "EAN-13"
    QR_CODE = "QR Code(2D)"
    PDF_417 = "PDF 417(2D)"
    DATA_MATRIX = "Data Matrix(2D)"
    CODE_39 = "Code 39"
    CODE_39_EXTENDED = "Code 39 Extended"
    CODE_93 = "Code 93"
    EAN_128_AUTO = "EAN 128 Auto"
    EAN_128_A = "EAN 128 A"
    EAN_128_B = "EAN 128 B"
    EAN_128_C = "EAN 128 C"
    GS1_128 = "GS1-128"
    GS1_DATA_MATRIX = "GS1 Data Matrix(2D)"
    GS1_QR_CODE = "GS1 QR Code(2D)"


class RFIDEncoderType(Enum):
    """RFID 编码器类型"""

    UHF = 0
    HF_15693 = 1
    HF_14443A = 2
    NFC = 3


class RFIDDataBlock(Enum):
    """RFID 数据块 (UHF)"""

    EPC = 0
    USER = 1
    # 注意：GJB/GBGM 的值可能不同，此处简化


class RFIDDataType(Enum):
    """RFID 数据类型"""

    TEXT = 0
    HEX = 1
    NDEF_URL = 2  # NDEF 网址链接 (HF/NFC)
    NDEF_TEXT = 3  # NDEF 纯文本 (HF/NFC)

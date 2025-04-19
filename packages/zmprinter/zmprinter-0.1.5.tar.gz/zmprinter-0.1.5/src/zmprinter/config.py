from typing import Optional

from .enums import PrinterStyle


class PrinterConfig:
    """打印机配置 (对应 C# ZMPrinter)"""

    def __init__(
        self,
        interface: PrinterStyle = PrinterStyle.USB,
        dpi: int = 300,
        speed: int = 4,
        darkness: int = 10,
        name: Optional[str] = None,  # 仅 DRIVER 模式需要
        ip_address: Optional[str] = None,  # 仅 NET 模式需要
        has_gap: bool = True,
        mbsn: Optional[str] = None,  # 指定USB打印机主板序号 (可选)
        page_direction: int = 1,  # 1 竖向，2 横向
        reverse: bool = False,  # 是否反向打印
        print_num: int = 1,  # 打印份数
        copy_num: int = 1,  # 副本份数
    ):
        self.interface = interface
        self.dpi = dpi
        self.speed = speed
        self.darkness = darkness
        self.name = name
        self.ip_address = ip_address
        self.has_gap = has_gap
        self.mbsn = mbsn
        self.page_direction = page_direction
        self.reverse = reverse
        self.print_num = print_num
        self.copy_num = copy_num


class LabelConfig:
    """标签配置 (对应 C# ZMLabel)"""

    def __init__(
        self,
        width: float = 60.0,
        height: float = 40.0,
        gap: float = 2.0,
        column_gap: float = 2.0,
        row_num: int = 1,
        column_num: int = 1,
        left_offset: float = 0.0,
        top_offset: float = 0.0,
        page_left_edges: float = 0.0,
        page_right_edges: float = 0.0,
        page_start_location: int = 0,
        page_label_order: int = 0,
        label_shape: int = 0,
    ):
        self.width = width  # 标签宽度，单位mm
        self.height = height  # 标签高度，单位mm
        self.gap = gap  # 行距，单位mm
        self.column_gap = column_gap  # 列距，单位mm
        self.row_num = row_num  # 行数
        self.column_num = column_num  # 列数
        self.left_offset = left_offset  # 左侧位置微调，单位mm
        self.top_offset = top_offset  # 顶部位置微调，单位mm
        self.page_left_edges = page_left_edges  # 左空，单位mm
        self.page_right_edges = page_right_edges  # 右空，单位mm
        self.page_start_location = page_start_location  # 起始位置，0为左上，1为右上，2为左下，3为右下
        self.page_label_order = page_label_order  # 标签顺序，0为水平，1为垂直
        self.label_shape = label_shape  # 标签的形状，0圆角矩形，1方角矩形，2椭圆形

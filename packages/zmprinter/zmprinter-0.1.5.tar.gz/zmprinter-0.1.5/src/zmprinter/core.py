import io
import sys
import platform
from pathlib import Path
from typing import List, Optional, Tuple

import clr
from PIL import Image

from .utils import get_logger
from .config import PrinterConfig, LabelConfig
from .enums import PrinterStyle, BarcodeType, RFIDEncoderType, RFIDDataBlock, RFIDDataType
from .elements import (
    LabelElement,
    TextElement,
    BarcodeElement,
    ImageElement,
    RFIDElement,
    ShapeElement,
    LabelElementType,
)
from .exceptions import (
    ZMPrinterSetupError,
    ZMPrinterImportError,
    ZMPrinterConfigError,
    ZMPrinterCommandError,
    ZMPrinterLSFError,
    ZMPrinterRFIDError,
    ZMPrinterRFIDReadError,
    ZMPrinterDataError,
)

# 获取logger实例
logger = get_logger(__name__)

clr.AddReference("System.Drawing")  # type: ignore
try:
    import System  # type: ignore
    from System.Collections.Generic import List as DotNetList  # type: ignore .NET List
    from System.Drawing import Bitmap as DotNetBitmap  # type: ignore .NET Drawing 命名空间
    from System.Drawing.Imaging import ImageFormat  # type: ignore
    from System.IO import MemoryStream  # type: ignore
except ImportError as e:
    logger.error(f"Failed to import System.Drawing: {e}")


class LabelPrinterSDK:
    """封装 LabelPrinter.dll 功能的 Python SDK"""

    def __init__(
        self,
        dll_path: Optional[str] = None,
        printer_config: Optional[PrinterConfig] = None,
        label_config: Optional[LabelConfig] = None,
    ):
        """
        初始化 SDK 并加载 DLL。
        :param dll_path: LabelPrinter.dll 的完整路径。如果为 None，会根据平台自动选择合适的DLL。
                       确保 DLL 依赖的 .NET Framework 版本已安装。
        """
        try:
            # 如果未提供路径，根据平台自动选择DLL
            if dll_path is None:
                # 获取当前模块所在目录路径
                module_dir = Path(__file__).parent

                # 根据平台特性选择合适的DLL目录
                if sys.platform == "win32":
                    if platform.architecture()[0] == "64bit":
                        # 64位Windows
                        dll_dir = "x64"
                    else:
                        # 32位Windows
                        dll_dir = "x86"
                else:
                    # 非Windows平台使用AnyCPU版本
                    dll_dir = "AnyCPU"

                # 构建DLL完整路径
                dll_path_obj = module_dir / "libs" / dll_dir / "LabelPrinter.dll"
                dll_path = str(dll_path_obj.resolve())
                logger.info(f"自动选择DLL路径: {dll_path}")

            # 检查文件是否存在
            if not Path(dll_path).exists():
                err_msg = f"找不到DLL文件: {dll_path}"
                logger.error(err_msg)
                raise ZMPrinterImportError(err_msg)

            # 加载DLL
            System.Reflection.Assembly.LoadFile(dll_path)
            clr.AddReference("LabelPrinter")  # type: ignore
        except (ImportError, FileNotFoundError, System.IO.FileNotFoundException, System.BadImageFormatException) as e:
            logger.error(f"无法加载或引用 LabelPrinter.dll: {e}")
            raise ZMPrinterImportError(
                f"无法加载 LabelPrinter.dll。请确保 DLL 存在、架构匹配且 .NET 环境配置正确。错误: {e}",
                original_exception=e,
            )
        except Exception as e:
            logger.error(f"无法加载 LabelPrinter.dll: {e}")
            raise ImportError(f"无法加载 LabelPrinter.dll。请确保 DLL 存在且 .NET 环境配置正确。错误: {e}")

        try:
            # 导入 .NET 命名空间和类
            import LabelPrinter  # type: ignore

            self.LabelPrinter = LabelPrinter

            # 实例化 .NET 工具类
            self.print_utility = self.LabelPrinter.PrintUtility()
            self.lsf_utility = self.LabelPrinter.LSFUtility()
            logger.info("LabelPrinter SDK 初始化成功")
        except ImportError as e:
            logger.error(f"成功加载 DLL 但无法导入 LabelPrinter 命名空间: {e}")
            raise ZMPrinterImportError(f"无法导入 LabelPrinter 命名空间。错误: {e}", original_exception=e)
        except Exception as e:
            logger.error(f"无法实例化 LabelPrinter 类: {e}")
            raise ZMPrinterSetupError(f"SDK 初始化失败: {e}", original_exception=e)

        self.printer_status = None
        self.printer_config = printer_config
        self.label_config = label_config

    def _create_dotnet_printer(self, config: PrinterConfig) -> object:
        """将 Python PrinterConfig 转换为 .NET ZMPrinter 对象"""
        try:
            dotnet_printer = self.LabelPrinter.ZMPrinter()
            dotnet_printer.printerinterface = self.LabelPrinter.PrinterStyle.Parse(
                self.LabelPrinter.PrinterStyle, config.interface.name
            )
            dotnet_printer.printerdpi = config.dpi
            dotnet_printer.printSpeed = config.speed
            dotnet_printer.printDarkness = config.darkness
            dotnet_printer.labelhavegap = config.has_gap
            if config.interface == PrinterStyle.DRIVER and config.name:
                dotnet_printer.printername = config.name
            elif (
                config.interface
                in [PrinterStyle.NET, PrinterStyle.RFID_NET, PrinterStyle.GBGM_NET, PrinterStyle.GJB_NET]
                and config.ip_address
            ):
                dotnet_printer.printernetip = config.ip_address
            if (
                config.interface
                in [PrinterStyle.USB, PrinterStyle.RFID_USB, PrinterStyle.GBGM_USB, PrinterStyle.GJB_USB]
                and config.mbsn
            ):
                dotnet_printer.printermbsn = config.mbsn
            dotnet_printer.pageDirection = config.page_direction
            dotnet_printer.reverse = config.reverse
            dotnet_printer.printnum = config.print_num
            dotnet_printer.copynum = config.copy_num
            return dotnet_printer
        except ValueError as e:
            raise ZMPrinterConfigError(f"无效的打印机接口类型: {config.interface.name}", original_exception=e)
        except AttributeError as e:
            raise ZMPrinterConfigError(f"打印机配置对象缺少必要属性: {e}", original_exception=e)
        except Exception as e:
            raise ZMPrinterConfigError(f"处理打印机配置时出错: {e}", original_exception=e)

    def _create_dotnet_label(self, config: LabelConfig) -> object:
        """将 Python LabelConfig 转换为 .NET ZMLabel 对象"""
        dotnet_label = self.LabelPrinter.ZMLabel()
        dotnet_label.labelwidth = config.width
        dotnet_label.labelheight = config.height
        dotnet_label.labelrowgap = config.gap
        dotnet_label.labelcolumngap = config.column_gap
        dotnet_label.labelrownum = config.row_num
        dotnet_label.labelcolumnnum = config.column_num
        dotnet_label.leftoffset = config.left_offset
        dotnet_label.topoffset = config.top_offset
        dotnet_label.pageleftedges = config.page_left_edges
        dotnet_label.pagerightedges = config.page_right_edges
        dotnet_label.pagestartlocation = config.page_start_location
        dotnet_label.pagelabelorder = config.page_label_order
        dotnet_label.labelshape = config.label_shape
        return dotnet_label

    def _create_dotnet_object_list(self, elements: List[LabelElementType]) -> object:
        """将 Python LabelElement 列表转换为 .NET List<LabelObject>"""
        elem = None
        try:
            # 需要显式指定泛型类型
            dotnet_list = DotNetList[self.LabelPrinter.LabelObject]()

            for elem in elements:
                dotnet_obj = self.LabelPrinter.LabelObject()
                dotnet_obj.ObjectName = elem.object_name
                # 对象名称的命名规则：
                # 1、条码对象以"barcode"开头，如"barcode-01"，"barcode-02"...
                # 2、文字对象以"text"开头，如"text-01"，"text-02"...
                # 3、直线对象以"line"开头，如"line-01"，"line-02"...
                # 4、矩形对象以"rectangle"开头，如"rectangle-01"，"rectangle-02"...
                # 5、图片对象以"image"开头，如"image-01"，"image-02"...
                # 6、RFID对象以"rfiduhf"开头，如"rfiduhf-01"，"rfiduhf-02"...注意：超高频和高频的对象名称都是以"rfiduhf"开头

                # 根据 Python 对象的类型设置 .NET 对象属性
                if isinstance(elem, TextElement):
                    # ObjectName 在C#示例中似乎包含类型信息，如 "text-01"
                    # 但 DLL 文档中 ObjectName 好像只是标识符。此处遵循 C# 示例给 object_name 赋值。
                    dotnet_obj.objectdata = elem.data
                    dotnet_obj.Xposition = elem.x
                    dotnet_obj.Yposition = elem.y
                    dotnet_obj.textfont = elem.font_name
                    dotnet_obj.fontsize = elem.font_size
                    dotnet_obj.fontstyle = elem.font_style
                    dotnet_obj.direction = elem.direction
                    dotnet_obj.blackbackground = elem.black_background
                    dotnet_obj.chargap = elem.char_gap
                    dotnet_obj.charHZoom = elem.char_h_zoom
                    dotnet_obj.texttype = elem.text_type
                    dotnet_obj.texttextalign = elem.text_text_align
                    dotnet_obj.texttextvalign = elem.text_text_valign
                    dotnet_obj.textwidth = elem.text_width
                    dotnet_obj.textwidthbeyound = elem.text_width_beyound
                    dotnet_obj.linegapindex = elem.line_gap_index
                    dotnet_obj.linegap = elem.line_gap
                    dotnet_obj.circularradius = elem.circular_radius
                    dotnet_obj.textradian = elem.text_radian
                    dotnet_obj.textstartangle = elem.text_start_angle
                    dotnet_obj.rewindingdirection = elem.rewinding_direction
                    dotnet_obj.literaldirection = elem.literal_direction

                elif isinstance(elem, BarcodeElement):
                    dotnet_obj.objectdata = elem.data
                    dotnet_obj.Xposition = elem.x
                    dotnet_obj.Yposition = elem.y
                    dotnet_obj.barcodekind = elem.barcode_type
                    dotnet_obj.barcodescale = elem.scale
                    dotnet_obj.direction = elem.direction

                    if elem.height is not None:  # 仅一维码设置
                        dotnet_obj.barcodeheight = elem.height

                    dotnet_obj.textposition = elem.text_position
                    dotnet_obj.errorcorrection = elem.error_correction
                    dotnet_obj.charencoding = elem.char_encoding
                    dotnet_obj.qrversion = elem.qr_version
                    dotnet_obj.code39widthratio = elem.code39_width_ratio
                    dotnet_obj.code39startchar = elem.code39_start_char
                    dotnet_obj.barcodealign = elem.barcode_align
                    dotnet_obj.pdf417_rows = elem.pdf417_rows
                    dotnet_obj.pdf417_columns = elem.pdf417_columns
                    dotnet_obj.pdf417_rows_auto = elem.pdf417_rows_auto
                    dotnet_obj.pdf417_columns_auto = elem.pdf417_columns_auto
                    dotnet_obj.datamatrixShape = elem.datamatrix_shape
                    dotnet_obj.textoffset = elem.text_offset
                    dotnet_obj.textalign = elem.text_align
                    dotnet_obj.textfont = elem.text_font
                    dotnet_obj.fontsize = elem.text_font_size

                elif isinstance(elem, ImageElement):
                    dotnet_obj.Xposition = elem.x
                    dotnet_obj.Yposition = elem.y
                    dotnet_obj.direction = elem.direction
                    dotnet_obj.transparent = elem.transparent

                    if elem.image_data:
                        # 将 Python bytes 转换为 .NET byte[]
                        dotnet_obj.imagedata = System.Array[System.Byte](elem.image_data)

                    dotnet_obj.aspectRatio = elem.aspect_ratio
                    dotnet_obj.hscale = elem.h_scale
                    dotnet_obj.vscale = elem.v_scale
                    dotnet_obj.imagefixedsize = elem.image_fixed_size
                    dotnet_obj.imagefixedwidth = elem.image_fixed_width
                    dotnet_obj.imagefixedheight = elem.image_fixed_height

                elif isinstance(elem, RFIDElement):
                    dotnet_obj.objectdata = elem.data
                    dotnet_obj.RFIDEncodertype = elem.rfid_encoder_type
                    dotnet_obj.RFIDDatablock = elem.rfid_data_block if elem.data_block else 0
                    dotnet_obj.RFIDDatatype = elem.rfid_data_type
                    dotnet_obj.RFIDTextencoding = elem.rfid_text_encoding
                    dotnet_obj.DataAlignment = elem.data_alignment
                    dotnet_obj.RFIDerrortimes = elem.rfid_error_times
                    dotnet_obj.Datalengthdoublewords = elem.data_length_double_words

                    # HF相关属性
                    dotnet_obj.HFstartblock = elem.hf_start_block
                    dotnet_obj.HFmodulepower = elem.hf_module_power
                    dotnet_obj.Encrypt14443A = elem.encrypt_14443a
                    dotnet_obj.Sector14443A = elem.sector_14443a
                    dotnet_obj.KEYAB14443A = elem.keyab_14443a
                    dotnet_obj.KEYAnewpwd = elem.keya_new_pwd
                    dotnet_obj.KEYAoldpwd = elem.keya_old_pwd
                    dotnet_obj.KEYBnewpwd = elem.keyb_new_pwd
                    dotnet_obj.KEYBoldpwd = elem.keyb_old_pwd
                    dotnet_obj.Encrypt14443AControl = elem.encrypt_14443a_control
                    dotnet_obj.Encrypt14443AControlvalue = elem.encrypt_14443a_control_value
                    dotnet_obj.Controlarea15693 = elem.control_area_15693
                    dotnet_obj.Controlvalue15693 = elem.control_value_15693

                elif isinstance(elem, ShapeElement):
                    dotnet_obj.startXposition = elem.start_x_position
                    dotnet_obj.startYposition = elem.start_y_position
                    dotnet_obj.endXposition = elem.end_x_position
                    dotnet_obj.endYposition = elem.end_y_position
                    dotnet_obj.lineWidth = elem.line_width
                    dotnet_obj.lineDashStyle = elem.line_dash_style
                    dotnet_obj.fillRectangle = elem.fill_rectangle
                    dotnet_obj.lineclass = elem.line_class
                    if elem.rectangle_class is not None:
                        dotnet_obj.rectangleclass = elem.rectangle_class
                    dotnet_obj.objectclass = elem.object_class

                dotnet_list.Add(dotnet_obj)

            return dotnet_list
        except (TypeError, ValueError, AttributeError) as e:
            raise ZMPrinterConfigError(
                f"处理标签元素 '{getattr(elem, 'object_name', '未知')}' 时数据无效: {e}", original_exception=e
            )

    def _convert_bitmap_to_pil(self, dotnet_bitmap: "DotNetBitmap") -> Optional["Image.Image"]:
        """将 .NET Bitmap 转换为 PIL Image 对象"""
        if dotnet_bitmap is None:
            return None
        try:
            stream = MemoryStream()
            # 以 PNG 格式保存到内存流，PNG 支持透明度且无损
            dotnet_bitmap.Save(stream, ImageFormat.Png)
            stream.Seek(0, System.IO.SeekOrigin.Begin)  # 重置流位置
            # 从内存流中读取 bytes
            image_bytes = stream.ToArray()
            stream.Close()
            # 使用 PIL 从 bytes 创建 Image 对象
            pil_image = Image.open(io.BytesIO(image_bytes))
            # 返回 PIL Image 对象（如果需要，可以 pil_image.copy() 防止原始 bytes 被回收）
            return pil_image.copy()
        except Exception as e:
            logger.error(f"转换 Bitmap 到 PIL Image 失败: {e}")
            raise ZMPrinterDataError("转换 .NET Bitmap 到 PIL Image 失败", original_exception=e)
        finally:
            # 确保释放 .NET Bitmap 对象
            if dotnet_bitmap is not None:
                dotnet_bitmap.Dispose()

    def preview_label(
        self,
        elements: List[LabelElementType],
        printer_config: Optional[PrinterConfig] = None,
        label_config: Optional[LabelConfig] = None,
    ) -> Optional["Image.Image"]:
        """
        生成标签预览图。
        :param printer_config: 打印机配置对象
        :param label_config: 标签配置对象
        :param elements: 标签元素列表
        :return: PIL Image 对象，如果生成失败则返回 None
        """
        if printer_config is None:
            printer_config = self.printer_config
            if printer_config is None:
                raise ZMPrinterCommandError("打印机配置对象为空")
        if label_config is None:
            label_config = self.label_config
            if label_config is None:
                raise ZMPrinterCommandError("标签配置对象为空")
        try:
            dotnet_printer = self._create_dotnet_printer(printer_config)
            dotnet_label = self._create_dotnet_label(label_config)
            dotnet_elements = self._create_dotnet_object_list(elements)

            # 调用 DLL 的 GetLabelImage 方法
            dotnet_bitmap = self.print_utility.GetLabelImage(
                dotnet_printer, dotnet_label, dotnet_elements, 0
            )  # 0 表示无边框

            # 转换 Bitmap 为 PIL Image
            return self._convert_bitmap_to_pil(dotnet_bitmap)
        except Exception as e:
            raise ZMPrinterCommandError(f"生成标签预览失败: {e}", original_exception=e)

    def print_label(
        self,
        elements: List[LabelElementType],
        copies: int = 1,
        stop_at_error: bool = True,
        printer_config: Optional[PrinterConfig] = None,
        label_config: Optional[LabelConfig] = None,
    ) -> Tuple[str, int]:
        """
        打印标签。
        :param elements: 标签元素列表
        :param copies: 打印份数。注意：DLL 的 PrintLabel 本身打印一张，循环在 Python 层完成。
        :param stop_at_error: 是否在遇到错误时停止打印。
        :param printer_config: 打印机配置对象
        :param label_config: 标签配置对象
        :return: 一个元组 (final_result, finished_count)。
        """
        if printer_config is None:
            printer_config = self.printer_config
            if printer_config is None:
                raise ZMPrinterCommandError("打印机配置对象为空")
        if label_config is None:
            label_config = self.label_config
            if label_config is None:
                raise ZMPrinterCommandError("标签配置对象为空")

        if copies < 1:
            return "Error: 打印份数必须至少为 1", 0

        final_result = "OK"  # 假设成功
        finished_count = 0

        for i in range(copies):
            logger.debug(f"准备打印第 {i + 1}/{copies} 张...")
            try:
                dotnet_printer = self._create_dotnet_printer(printer_config)
                dotnet_label = self._create_dotnet_label(label_config)
                dotnet_elements = self._create_dotnet_object_list(elements)

                # 调用 DLL 的 PrintLabel 方法
                # C# 方法签名: string PrintLabel(ZMPrinter printer, ZMLabel label, List<LabelObject> elements, bool firstlabel, bool lastlabel)
                # 分析源码后发现 firstlabel 和 lastlabel 并未实际使用
                return_msg = self.print_utility.PrintLabel(dotnet_printer, dotnet_label, dotnet_elements, True, True)

                if isinstance(return_msg, str) and return_msg.startswith("Error:"):
                    logger.error(f"打印第 {i + 1} 张时出错: {return_msg}")
                    final_result = return_msg  # 记录第一个错误
                    if stop_at_error:
                        break  # 如果出错则停止后续打印
                else:
                    logger.debug(f"第 {i + 1}/{copies} 张标签指令已发送")
                    finished_count += 1

            except Exception as e:
                error_msg = f"打印第 {i + 1} 张时发生 Python 异常: {e}"
                logger.exception(error_msg)
                final_result = f"Error: {error_msg}"
                break  # 停止后续打印

        return final_result, finished_count

    def read_lsf(
        self, lsf_file_path: str | Path
    ) -> Tuple[Optional[PrinterConfig], Optional[LabelConfig], Optional[List[LabelElementType]], str]:
        """
        读取 LSF 标签文件。
        :param lsf_file_path: LSF 文件的完整路径。
        :return: 一个元组 (printer_config, label_config, elements, status_message)。
                 如果成功，返回解析出的配置和元素列表，状态消息为空字符串。
                 如果失败，返回 None, None, None 和错误消息。
        """
        try:
            # 创建 .NET 对象的引用，LSFUtility.OpenLabel 会修改它们
            dotnet_printer_ref = self.LabelPrinter.ZMPrinter()
            dotnet_label_ref = self.LabelPrinter.ZMLabel()
            dotnet_elements_ref = DotNetList[self.LabelPrinter.LabelObject]()

            # 调用 OpenLabel。注意 pythonnet 如何处理 ref 参数 (通常直接传递对象即可，它会自动处理)
            # C# 签名: string OpenLabel(string filename, ref ZMPrinter printer, ref ZMLabel label, ref List<LabelObject> elements)
            status_message, _, _, elements_ref = self.lsf_utility.OpenLabel(
                str(lsf_file_path), dotnet_printer_ref, dotnet_label_ref, dotnet_elements_ref
            )

            if isinstance(status_message, str) and status_message:  # 如果返回了非空字符串，表示有错误
                raise ZMPrinterLSFError(f"Error: {status_message}")

            # ---- 将 .NET 对象转换回 Python 对象 ----

            # 转换 PrinterConfig
            # 注意：接口类型需要从 .NET 枚举转回 Python 枚举
            interface_val = dotnet_printer_ref.printerinterface.value__  # 获取枚举的整数值
            py_interface = PrinterStyle(interface_val)
            printer_config = PrinterConfig(
                interface=py_interface,
                dpi=dotnet_printer_ref.printerdpi,
                speed=dotnet_printer_ref.printSpeed,
                darkness=dotnet_printer_ref.printDarkness,
                name=dotnet_printer_ref.printername if dotnet_printer_ref.printername else None,
                ip_address=dotnet_printer_ref.printernetip if dotnet_printer_ref.printernetip else None,
                has_gap=dotnet_printer_ref.labelhavegap,
                mbsn=dotnet_printer_ref.printermbsn,
                page_direction=dotnet_printer_ref.pageDirection,
                reverse=dotnet_printer_ref.reverse,
                print_num=dotnet_printer_ref.printnum,
                copy_num=dotnet_printer_ref.copynum,
            )

            # 转换 LabelConfig
            label_config = LabelConfig(
                width=dotnet_label_ref.labelwidth,
                height=dotnet_label_ref.labelheight,
                gap=dotnet_label_ref.labelrowgap,
                column_gap=dotnet_label_ref.labelcolumngap,
                row_num=dotnet_label_ref.labelrownum,
                column_num=dotnet_label_ref.labelcolumnnum,
                left_offset=dotnet_label_ref.leftoffset,
                top_offset=dotnet_label_ref.topoffset,
                page_left_edges=dotnet_label_ref.pageleftedges,
                page_right_edges=dotnet_label_ref.pagerightedges,
                page_start_location=dotnet_label_ref.pagestartlocation,
                page_label_order=dotnet_label_ref.pagelabelorder,
                label_shape=dotnet_label_ref.labelshape,
            )

            # 转换 LabelElement 列表 (这部分比较复杂，需要反向映射)
            try:
                elements = []
                for dotnet_obj in elements_ref:
                    # **重要的假设**: 我们需要一种方法来确定 .NET LabelObject 对应哪个 Python LabelElement 类型。
                    # LSF 文件格式未知，可能需要根据 objectName 或 objectclass 来判断。
                    # 这里我们做一个简化的尝试，主要基于 objectName 或 objectclass。
                    # 更好的方法可能是在 LSF 文件中或 DLL 返回的对象中有更明确的类型指示。
                    object_name = dotnet_obj.ObjectName
                    object_data = dotnet_obj.objectdata  # TODO: 为空，暂时不清楚原因
                    x_pos = dotnet_obj.Xposition
                    y_pos = dotnet_obj.Yposition

                    py_element = None

                    # 尝试判断类型
                    if object_name.startswith("text"):
                        is_multiline = dotnet_obj.texttype == 1
                        py_element = TextElement(
                            object_name=object_name,
                            data=object_data,
                            x=x_pos,
                            y=y_pos,
                            font_name=dotnet_obj.textfont,
                            font_size=dotnet_obj.fontsize,
                            font_style=dotnet_obj.fontstyle,
                            is_multiline=is_multiline,
                            text_align=dotnet_obj.texttextalign,
                            text_valign=dotnet_obj.texttextvalign,
                            width=dotnet_obj.textwidth if is_multiline else None,
                            width_handling=dotnet_obj.textwidthbeyound if is_multiline else 0,
                        )

                        # 设置其他属性
                        if hasattr(dotnet_obj, "direction"):
                            py_element.direction = dotnet_obj.direction
                        if hasattr(dotnet_obj, "blackbackground"):
                            py_element.black_background = dotnet_obj.blackbackground
                        if hasattr(dotnet_obj, "chargap"):
                            py_element.char_gap = dotnet_obj.chargap
                        if hasattr(dotnet_obj, "charHZoom"):
                            py_element.char_h_zoom = dotnet_obj.charHZoom
                        if hasattr(dotnet_obj, "linegapindex"):
                            py_element.line_gap_index = dotnet_obj.linegapindex
                        if hasattr(dotnet_obj, "linegap"):
                            py_element.line_gap = dotnet_obj.linegap

                        # 圆形文字相关属性
                        if dotnet_obj.texttype == 2:  # 圆形环绕文字
                            py_element.text_type = 2
                            if hasattr(dotnet_obj, "circularradius"):
                                py_element.circular_radius = dotnet_obj.circularradius
                            if hasattr(dotnet_obj, "textradian"):
                                py_element.text_radian = dotnet_obj.textradian
                            if hasattr(dotnet_obj, "textstartangle"):
                                py_element.text_start_angle = dotnet_obj.textstartangle
                            if hasattr(dotnet_obj, "rewindingdirection"):
                                py_element.rewinding_direction = dotnet_obj.rewindingdirection
                            if hasattr(dotnet_obj, "literaldirection"):
                                py_element.literal_direction = dotnet_obj.literaldirection

                    elif object_name.startswith("barcode"):  # 可能是条码
                        # 将字符串转回可能的枚举，如果需要的话，或者直接用字符串
                        barcode_type_str = dotnet_obj.barcodekind
                        try:
                            barcode_type_enum = BarcodeType(barcode_type_str)
                        except ValueError:
                            barcode_type_enum = barcode_type_str  # 如果不在枚举中，保留字符串

                        py_element = BarcodeElement(
                            object_name=object_name,
                            data=object_data,
                            barcode_type=barcode_type_enum,
                            x=x_pos,
                            y=y_pos,
                            scale=dotnet_obj.barcodescale,
                            height=dotnet_obj.barcodeheight
                            if hasattr(dotnet_obj, "barcodeheight") and dotnet_obj.barcodeheight > 0
                            else None,
                            text_position=dotnet_obj.textposition,
                            direction=dotnet_obj.direction,
                            text_font_size=dotnet_obj.fontsize,
                        )

                        # 设置其他属性
                        if hasattr(dotnet_obj, "errorcorrection"):
                            py_element.error_correction = dotnet_obj.errorcorrection
                        if hasattr(dotnet_obj, "charencoding"):
                            py_element.char_encoding = dotnet_obj.charencoding
                        if hasattr(dotnet_obj, "qrversion"):
                            py_element.qr_version = dotnet_obj.qrversion
                        if hasattr(dotnet_obj, "code39widthratio"):
                            py_element.code39_width_ratio = dotnet_obj.code39widthratio
                        if hasattr(dotnet_obj, "code39startchar"):
                            py_element.code39_start_char = dotnet_obj.code39startchar
                        if hasattr(dotnet_obj, "barcodealign"):
                            py_element.barcode_align = dotnet_obj.barcodealign
                        if hasattr(dotnet_obj, "pdf417_rows"):
                            py_element.pdf417_rows = dotnet_obj.pdf417_rows
                        if hasattr(dotnet_obj, "pdf417_columns"):
                            py_element.pdf417_columns = dotnet_obj.pdf417_columns
                        if hasattr(dotnet_obj, "pdf417_rows_auto"):
                            py_element.pdf417_rows_auto = dotnet_obj.pdf417_rows_auto
                        if hasattr(dotnet_obj, "pdf417_columns_auto"):
                            py_element.pdf417_columns_auto = dotnet_obj.pdf417_columns_auto
                        if hasattr(dotnet_obj, "datamatrixShape"):
                            py_element.datamatrix_shape = dotnet_obj.datamatrixShape
                        if hasattr(dotnet_obj, "textoffset"):
                            py_element.text_offset = dotnet_obj.textoffset
                        if hasattr(dotnet_obj, "textalign"):
                            py_element.text_align = dotnet_obj.textalign
                        if hasattr(dotnet_obj, "textfont"):
                            py_element.text_font = dotnet_obj.textfont
                        if hasattr(dotnet_obj, "fontsize"):
                            py_element.text_font_size = dotnet_obj.fontsize

                    elif object_name.startswith("image"):
                        # LSF 不太可能直接包含 imagedata，但如果 DLL 解析后填充了，可以处理
                        py_element = ImageElement(
                            object_name=object_name,
                            image_data=bytes(dotnet_obj.imagedata),  # .NET byte[] to Python bytes
                            x=x_pos,
                            y=y_pos,
                            fixed_width=dotnet_obj.imagefixedwidth if dotnet_obj.imagefixedsize else None,
                            fixed_height=dotnet_obj.imagefixedheight if dotnet_obj.imagefixedsize else None,
                        )

                        # 设置其他属性
                        if hasattr(dotnet_obj, "direction"):
                            py_element.direction = dotnet_obj.direction
                        if hasattr(dotnet_obj, "transparent"):
                            py_element.transparent = dotnet_obj.transparent
                        if hasattr(dotnet_obj, "aspectRatio"):
                            py_element.aspect_ratio = dotnet_obj.aspectRatio
                        if hasattr(dotnet_obj, "hscale"):
                            py_element.h_scale = dotnet_obj.hscale
                        if hasattr(dotnet_obj, "vscale"):
                            py_element.v_scale = dotnet_obj.vscale
                        py_element.image_fixed_size = dotnet_obj.imagefixedsize

                    elif object_name.startswith("rfiduhf"):  # 可能是 RFID
                        # 根据 encoder_type 区分 UHF/HF
                        encoder_type = RFIDEncoderType(dotnet_obj.RFIDEncodertype)
                        data_type = RFIDDataType(dotnet_obj.RFIDDatatype)
                        data_block = (
                            RFIDDataBlock(dotnet_obj.RFIDDatablock) if encoder_type == RFIDEncoderType.UHF else None
                        )
                        hf_start_block = dotnet_obj.HFstartblock if encoder_type != RFIDEncoderType.UHF else 0

                        py_element = RFIDElement(
                            object_name=object_name,
                            data=object_data,
                            rfid_encoder_type=encoder_type,
                            rfid_data_block=data_block,
                            rfid_data_type=data_type,
                            rfid_error_times=dotnet_obj.RFIDerrortimes,
                            hf_start_block=hf_start_block,
                        )

                        # 设置其他属性
                        # UHF相关属性
                        py_element.rfid_encoder_type = dotnet_obj.RFIDEncodertype
                        py_element.rfid_data_block = (
                            dotnet_obj.RFIDDatablock if encoder_type == RFIDEncoderType.UHF else 0
                        )
                        py_element.rfid_data_type = dotnet_obj.RFIDDatatype
                        if hasattr(dotnet_obj, "RFIDTextencoding"):
                            py_element.rfid_text_encoding = dotnet_obj.RFIDTextencoding
                        if hasattr(dotnet_obj, "DataAlignment"):
                            py_element.data_alignment = dotnet_obj.DataAlignment
                        py_element.rfid_error_times = dotnet_obj.RFIDerrortimes
                        if hasattr(dotnet_obj, "Datalengthdoublewords"):
                            py_element.data_length_double_words = dotnet_obj.Datalengthdoublewords

                        # HF相关属性
                        if hasattr(dotnet_obj, "HFmodulepower"):
                            py_element.hf_module_power = dotnet_obj.HFmodulepower
                        if hasattr(dotnet_obj, "Encrypt14443A"):
                            py_element.encrypt_14443a = dotnet_obj.Encrypt14443A
                        if hasattr(dotnet_obj, "Sector14443A"):
                            py_element.sector_14443a = dotnet_obj.Sector14443A
                        if hasattr(dotnet_obj, "KEYAB14443A"):
                            py_element.keyab_14443a = dotnet_obj.KEYAB14443A
                        if hasattr(dotnet_obj, "KEYAnewpwd"):
                            py_element.keya_new_pwd = dotnet_obj.KEYAnewpwd
                        if hasattr(dotnet_obj, "KEYAoldpwd"):
                            py_element.keya_old_pwd = dotnet_obj.KEYAoldpwd
                        if hasattr(dotnet_obj, "KEYBnewpwd"):
                            py_element.keyb_new_pwd = dotnet_obj.KEYBnewpwd
                        if hasattr(dotnet_obj, "KEYBoldpwd"):
                            py_element.keyb_old_pwd = dotnet_obj.KEYBoldpwd
                        if hasattr(dotnet_obj, "Encrypt14443AControl"):
                            py_element.encrypt_14443a_control = dotnet_obj.Encrypt14443AControl
                        if hasattr(dotnet_obj, "Encrypt14443AControlvalue"):
                            py_element.encrypt_14443a_control_value = dotnet_obj.Encrypt14443AControlvalue
                        if hasattr(dotnet_obj, "Controlarea15693"):
                            py_element.control_area_15693 = dotnet_obj.Controlarea15693
                        if hasattr(dotnet_obj, "Controlvalue15693"):
                            py_element.control_value_15693 = dotnet_obj.Controlvalue15693

                    elif object_name.startswith("line") or object_name.startswith("rectangle"):
                        shape_type = "line" if dotnet_obj.objectclass == 1 else "rectangle"
                        py_element = ShapeElement(
                            object_name=object_name,
                            shape_type=shape_type,
                            start_x=dotnet_obj.startXposition,
                            start_y=dotnet_obj.startYposition,
                            end_x=dotnet_obj.endXposition,
                            end_y=dotnet_obj.endYposition,
                            line_width=dotnet_obj.lineWidth,
                        )

                        # 设置其他属性
                        py_element.start_x_position = dotnet_obj.startXposition
                        py_element.start_y_position = dotnet_obj.startYposition
                        py_element.end_x_position = dotnet_obj.endXposition
                        py_element.end_y_position = dotnet_obj.endYposition
                        if hasattr(dotnet_obj, "lineDashStyle"):
                            py_element.line_dash_style = dotnet_obj.lineDashStyle
                        if hasattr(dotnet_obj, "fillRectangle"):
                            py_element.fill_rectangle = dotnet_obj.fillRectangle
                        if hasattr(dotnet_obj, "lineclass") and shape_type == "line":
                            py_element.line_class = dotnet_obj.lineclass
                        if hasattr(dotnet_obj, "rectangleclass") and shape_type == "rectangle":
                            py_element.rectangle_class = dotnet_obj.rectangleclass
                        py_element.object_class = dotnet_obj.objectclass

                    if py_element:
                        # 处理 LSF 特有的变量
                        if (
                            hasattr(dotnet_obj, "Variables")
                            and dotnet_obj.Variables is not None
                            and dotnet_obj.Variables.Count > 0
                        ):
                            py_element.variables = []  # 添加一个列表来存储变量信息
                            for var in dotnet_obj.Variables:
                                # LSF 的变量结构未知，假设它有 'sharename' 和 'data' 属性
                                py_element.variables.append(
                                    {"sharename": getattr(var, "sharename", ""), "data": getattr(var, "data", "")}
                                )

                        elements.append(py_element)
                    else:
                        logger.warning(f"警告: 无法识别 LSF 文件中的对象 '{object_name}'")
            except (AttributeError, ValueError, KeyError, IndexError) as e:
                logger.exception("将 .NET LSF 对象转换为 Python 对象时出错")
                raise ZMPrinterLSFError(f"解析 LSF 文件内部数据结构失败: {e}", original_exception=e)

            return printer_config, label_config, elements, ""
        except ZMPrinterLSFError:
            raise
        except FileNotFoundError as e:  # 如果 OpenLabel 不处理文件不存在的情况
            raise ZMPrinterLSFError(f"LSF 文件未找到: {lsf_file_path}", original_exception=e)
        except Exception as e:
            return None, None, None, f"Error: 读取 LSF 文件时发生 Python 异常: {e}"

    def update_element_data(self, elements: List[LabelElementType], object_name: str, new_data: str):
        """
        更新标签元素列表(Python 对象列表)中指定名称的元素的数据。
        这主要用于在打印前修改从 LSF 文件读取或手动创建的元素。
        :param elements: 标签元素列表 (Python 对象)
        :param object_name: 要更新的元素的 object_name
        :param new_data: 新的数据值
        :return: True 如果找到并更新成功，False 如果未找到该元素
        """
        found = False
        for elem in elements:
            if elem.object_name == object_name:
                elem.data = new_data
                found = True
                # 注意：如果 LSF 变量也需要更新，这里的逻辑需要更复杂
                # 需要检查 elem.variables 并根据 sharename 更新
                if hasattr(elem, "variables") and elem.variables:
                    var_updated = False
                    for var_info in elem.variables:
                        # 假设 LSF 变量的 sharename 就是 object_name (或者需要其他逻辑)
                        if var_info.get("sharename") == object_name:
                            var_info["data"] = new_data
                            var_updated = True
                            break
                    if not var_updated:
                        logger.warning(f"更新了元素 '{object_name}' 的主数据，但未找到同名的 LSF 变量进行更新。")
            # break # 如果确定 object_name 是唯一的，可以 break
            # LSF 文件中可能有多个对象使用相同的 '子字符串共享名称'
            elif hasattr(elem, "variables") and elem.variables:
                for var_info in elem.variables:
                    if var_info.get("sharename") == object_name:
                        var_info["data"] = new_data
                        found = True  # 标记找到了一个需要更新的变量
                        # 这里不 break，因为其他元素可能也有同名变量

        return found

    def read_uhf_tag(
        self,
        area: int = 0,
        power: int = 0,
        stop_position: int = 2,
        timeout: int = 2000,
        printer_config: Optional[PrinterConfig] = None,
        label_config: Optional[LabelConfig] = None,
    ) -> str:
        """
        读取超高频 RFID 标签数据 (TID, EPC, 或两者)。
        :param printer_config: 打印机配置 (接口必须是 RFID_USB 或 RFID_NET)
        :param label_config: 标签配置
        :param area: 读取区域 (0: TID, 1: EPC, 2: TID+EPC)
        :param power: 读取功率 (0-25 dBm, 0 表示使用打印机当前设置)
        :param stop_position: 读取后标签停止位置 (0:原始, 1:撕纸, 2:打印, 3:写入)
        :param timeout: 超时时间 (毫秒)
        :return: 读取到的数据 (成功)
        """
        if printer_config is None:
            printer_config = self.printer_config
            if printer_config is None:
                raise ZMPrinterCommandError("打印机配置对象为空")
        if label_config is None:
            label_config = self.label_config
            if label_config is None:
                raise ZMPrinterCommandError("标签配置对象为空")

        if printer_config.interface not in [
            PrinterStyle.RFID_USB,
            PrinterStyle.RFID_NET,
            PrinterStyle.GBGM_USB,
            PrinterStyle.GBGM_NET,
            PrinterStyle.GJB_USB,
            PrinterStyle.GJB_NET,
        ]:
            raise ZMPrinterConfigError("打印机接口必须兼容RFID才能读取UHF标签。")
        try:
            dotnet_printer = self._create_dotnet_printer(printer_config)
            dotnet_label = self._create_dotnet_label(label_config)

            # C# 签名: string GetUHFTagData(ZMPrinter printer, ZMLabel label, int area, int power, int stopPosition, int timeout)
            tag_data = self.print_utility.GetUHFTagData(
                dotnet_printer, dotnet_label, area, power, stop_position, timeout
            )

            if tag_data is None:
                raise ZMPrinterRFIDReadError("读取 RFID 标签失败", dll_message=tag_data)
            elif isinstance(tag_data, str) and tag_data.startswith("Error:"):
                raise ZMPrinterRFIDReadError("读取 RFID 标签失败", dll_message=tag_data)
            else:
                return tag_data

        except Exception as e:
            raise ZMPrinterRFIDError(f"读取 RFID 标签时发生 Python 异常: {e}", original_exception=e)

    def read_hf_tag(
        self,
        protocol: int = 1,
        area: int = 0,
        power: int = 0,
        stop_position: int = 1,
        timeout: int = 2000,
        printer_config: Optional[PrinterConfig] = None,
        label_config: Optional[LabelConfig] = None,
    ) -> str:
        """
        读取高频 RFID 标签数据 (UID 或数据区)。
        :param printer_config: 打印机配置 (接口必须是 RFID_USB 或 RFID_NET)
        :param label_config: 标签配置
        :param protocol: 协议类型 (1: 15693, 2: 14443A, 3: NFC)
        :param area: 读取区域 (0: UID, 1: 数据区)
        :param power: 读取功率 (0: 12db, 1: 24db, 2: 36db, 3: 48db) - 文档中的值
        :param stop_position: 读取后标签停止位置 (0: 打印头下方, 1: 撕纸口) - 文档中的值
        :param timeout: 超时时间 (毫秒)
        :return: 读取到的数据 (成功) 或 "Error: xxx" (失败) 或空字符串 (未读到)
        """
        if printer_config is None:
            printer_config = self.printer_config
            if printer_config is None:
                raise ZMPrinterCommandError("打印机配置对象为空")
        if label_config is None:
            label_config = self.label_config
            if label_config is None:
                raise ZMPrinterCommandError("标签配置对象为空")

        if printer_config.interface not in [PrinterStyle.RFID_USB, PrinterStyle.RFID_NET]:  # 确认支持的接口类型
            raise ZMPrinterConfigError("打印机接口必须兼容RFID才能读取HF标签。")
        try:
            dotnet_printer = self._create_dotnet_printer(printer_config)
            dotnet_label = self._create_dotnet_label(label_config)

            # C# 签名: string GetHFTagData(ZMPrinter printer, ZMLabel label, int protocol, int area, int power, int stopPosition, int timeout)
            tag_data = self.print_utility.GetHFTagData(
                dotnet_printer, dotnet_label, protocol, area, power, stop_position, timeout
            )

            if tag_data is None:
                raise ZMPrinterRFIDReadError("读取 RFID 标签失败", dll_message=tag_data)
            elif isinstance(tag_data, str) and tag_data.startswith("Error:"):
                raise ZMPrinterRFIDReadError("读取 RFID 标签失败", dll_message=tag_data)
            else:
                return tag_data
        except Exception as e:
            raise ZMPrinterRFIDError(f"读取 HF 标签时发生 Python 异常: {e}", original_exception=e)

    def print_blank_page(
        self,
        print_error_mark: bool = True,
        printer_config: Optional[PrinterConfig] = None,
        label_config: Optional[LabelConfig] = None,
    ):
        """
        打印一个空白页，通常在 RFID 读取失败后用于排出标签。
        :param printer_config: 打印机配置
        :param label_config: 标签配置
        :param print_error_mark: 是否在空白页上打印错误标记 'X'
        """
        if printer_config is None:
            printer_config = self.printer_config
            if printer_config is None:
                raise ZMPrinterCommandError("打印机配置对象为空")
        if label_config is None:
            label_config = self.label_config
            if label_config is None:
                raise ZMPrinterCommandError("标签配置对象为空")
        try:
            dotnet_printer = self._create_dotnet_printer(printer_config)
            dotnet_label = self._create_dotnet_label(label_config)
            # C# 签名: void PrintaBlankpage(ZMPrinter printer, ZMLabel label, int printErrorFlag)
            self.print_utility.PrintaBlankpage(dotnet_printer, dotnet_label, 1 if print_error_mark else 0)
        except Exception as e:
            logger.exception(f"Error: 打印空白页时发生 Python 异常: {e}")
            raise ZMPrinterCommandError(f"打印空白页失败: {e}", original_exception=e)

    def get_printer_status(self, printer_config: Optional[PrinterConfig] = None) -> Tuple[int, str]:
        """
        获取打印机状态码和描述信息。
        :param printer_config: 打印机配置
        :return: 元组 (status_code, status_message)
                 status_code: 整数状态码 (见文档)
                 status_message: 状态码对应的描述或错误信息
        """
        if printer_config is None:
            printer_config = self.printer_config
            if printer_config is None:
                raise ZMPrinterCommandError("打印机配置对象为空")
        try:
            dotnet_printer = self._create_dotnet_printer(printer_config)
            # C# 签名: int getPrinterStatusCode(ZMPrinter printer)
            status_code = self.print_utility.getPrinterStatusCode(dotnet_printer)

            status_message = "未知状态"
            if status_code == 0:
                status_message = "打印机正常待机"
            elif status_code == 1:
                status_message = "指令语法错误"
            elif status_code == 4:
                status_message = "正在打印"
            elif status_code == 81:
                status_message = "硬件故障"
            elif status_code == 82:
                status_message = "碳带出错"
            elif status_code == 83:
                status_message = "标签出错"
            elif status_code == 88:
                status_message = "打印机暂停状态"
            elif status_code == 89:
                status_message = "标签用完"
            elif status_code == 90:
                status_message = "RFID读写出错"
            elif status_code == 91:
                status_message = "RFID程序校准出错"
            elif status_code == 92:
                status_message = "RFID手动校准出错"
            elif status_code == 96:
                status_message = "剥纸器正在等待取走标签"
            elif status_code == 99:
                status_message = "打印机刚完成升级 (状态 99)"
            elif status_code == 120:
                status_message = "打印机刚完成升级 (状态 120)"
            elif status_code == -101:
                status_message = "打印机硬件路径为空 (未连接?)"
            elif status_code == -102:
                status_message = "打开USB设备出错 (未连接?)"
            elif status_code == -103:
                status_message = "从USB读取状态失败 (异常?)"
            elif status_code == -104:
                status_message = "从USB读取状态异常 (异常?)"
            else:
                status_message = f"未知状态码: {status_code}"

            return status_code, status_message

        except Exception as e:
            return -999, f"Error: 获取状态时发生 Python 异常: {e}"  # 使用 -999 表示 SDK 内部错误

    def get_usb_printer_sn(self) -> List[str]:
        """
        获取当前连接的所有 USB 打印机的主板序列号。
        :return: 包含序列号的字符串列表。
        """
        try:
            # C# 签名: List<string> getUSBPrinterMainboardSN()
            dotnet_sn_list = self.print_utility.getUSBPrinterMainboardSN()
            # 将 .NET List<string> 转换为 Python list[str]
            return [sn for sn in dotnet_sn_list]
        except Exception as e:
            logger.exception(f"获取 USB SN 时发生异常: {e}")
            return []

    def send_printer_command(
        self,
        command_string: str,
        printer_config: Optional[PrinterConfig] = None,
    ) -> str:
        """
        直接向打印机发送原始指令字符串。
        :param printer_config: 打印机配置
        :param command_string: 要发送的打印机指令 (如 ZPL, EPL, TSPL, ZMPCLE)
        :return: DLL 返回的操作状态或错误信息。
        """
        if printer_config is None:
            printer_config = self.printer_config
            if printer_config is None:
                raise ZMPrinterCommandError("打印机配置对象为空")
        try:
            dotnet_printer = self._create_dotnet_printer(printer_config)
            # C# 签名: string SetPrinterParams(ZMPrinter printer, string paramstring)
            return_msg = self.print_utility.SetPrinterParams(dotnet_printer, command_string)
            return return_msg if return_msg is not None else ""
        except Exception as e:
            raise ZMPrinterCommandError(f"发送指令时发生 Python 异常: {e}", original_exception=e)

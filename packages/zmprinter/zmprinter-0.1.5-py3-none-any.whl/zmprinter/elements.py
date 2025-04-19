import base64
import binascii
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any, Union, Literal, cast

from .utils import get_logger
from .enums import BarcodeType, RFIDEncoderType, RFIDDataBlock, RFIDDataType

logger = get_logger(__name__)


class LabelElement:
    """标签元素基类 (对应 C# LabelObject 的通用部分)"""

    def __init__(
        self,
        object_name: str,  # 用于标识和更新元素
        x: float = 3.0,
        y: float = 3.0,
        data: Optional[str] = None,
    ):
        self.object_name = object_name
        self.x = x
        self.y = y
        self.data = data  # 通用数据字段
        self.direction = 0  # 旋转方向，0是0度，1是90度，2是180度，3是270度
        self.variables = []  # 存储LSF变量信息
        self.transparent = True  # 是否背景透明

    @classmethod
    def from_data(
        cls, data: Dict[str, Any]
    ) -> "TextElement | BarcodeElement | ImageElement | RFIDElement | ShapeElement":
        """
        从字典创建 LabelElement 对象。
        根据 ObjectName 的前缀判断元素类型并实例化相应的子类。

        :param data: 包含元素属性字典的列表。
                          字典的键应遵循 C# LabelObject 的属性名 (e.g., "ObjectName", "Xposition", "textfont")。
        :return: 一个包含实例化的 LabelElement 子类对象的列表。
        """
        object_name = data.get("ObjectName")
        if not object_name:
            raise ValueError(f"警告: 跳过缺少 'ObjectName' 的元素数据: {data}")

        element: Optional[LabelElement] = None
        obj_data = data.get("objectdata", "")  # Default to empty string if missing
        x_pos = float(data.get("Xposition", 3.0))  # Default position
        y_pos = float(data.get("Yposition", 3.0))  # Default position

        # --- Determine type based on ObjectName prefix ---
        if object_name.lower().startswith("text"):
            # --- Create TextElement ---
            font_size = float(data.get("fontsize", 10.0))
            # Handle potential multiline based on properties (a bit heuristic)
            # C# texttype: 0=single, 1=paragraph, 2=circular
            text_type = int(data.get("texttype", 0))
            is_multiline = text_type == 1
            width = float(data.get("textwidth", 30.0)) if is_multiline else None

            element = TextElement(
                object_name=object_name,
                data=obj_data,
                x=x_pos,
                y=y_pos,
                font_name=data.get("textfont", "黑体"),
                font_size=font_size,
                font_style=cast(Literal[0, 1, 2, 3], int(data.get("fontstyle", 0))),
                text_align=cast(Literal[0, 1, 2], int(data.get("texttextalign", 0))),  # Map C# texttextalign
                text_valign=cast(Literal[0, 1, 2], int(data.get("texttextvalign", 0))),  # Map C# texttextvalign
                is_multiline=is_multiline,
                width=width,
                width_handling=cast(Literal[0, 1, 2], int(data.get("textwidthbeyound", 0))) if is_multiline else 0,
                black_background=bool(data.get("blackbackground", False)),
                char_gap=float(data.get("chargap", 0)),
                char_h_zoom=float(data.get("charHZoom", 1)),
                line_gap_index=cast(Literal[0, 1, 2, 3], int(data.get("linegapindex", 0))),
                line_gap=float(data.get("linegap", 0)),
                # Circular text properties (if texttype == 2)
                circular_radius=float(data.get("circularradius", 2.0)),
                text_radian=int(data.get("textradian", 360)),
                text_start_angle=int(data.get("textstartangle", 0)),
                rewinding_direction=cast(Literal[0, 1], int(data.get("rewindingdirection", 0))),
                literal_direction=cast(Literal[0, 1], int(data.get("literaldirection", 0))),
            )
            # Explicitly set text_type if circular
            if text_type == 2:
                element.text_type = 2

        elif object_name.lower().startswith("barcode"):
            # --- Create BarcodeElement ---
            barcode_kind_str = data.get("barcodekind", "Code 128 Auto")
            try:
                # Try to convert string to BarcodeType Enum
                barcode_type_enum = BarcodeType(barcode_kind_str)
            except ValueError:
                # If not in Enum, keep the string (might be a custom type)
                barcode_type_enum = barcode_kind_str

            height_val = data.get("barcodeheight")
            height = float(height_val) if height_val is not None and float(height_val) > 0 else None

            element = BarcodeElement(
                object_name=object_name,
                data=obj_data,
                barcode_type=barcode_type_enum,
                x=x_pos,
                y=y_pos,
                scale=float(data.get("barcodescale", 3)),
                height=height,
                text_position=cast(Literal[0, 1, 2], int(data.get("textposition", 0))),
                direction=cast(Literal[0, 1, 2, 3], int(data.get("direction", 0))),
                error_correction=cast(Literal[0, 1, 2, 3], int(data.get("errorcorrection", 0))),
                char_encoding=cast(Literal[0, 1], int(data.get("charencoding", 0))),
                qr_version=int(data.get("qrversion", 0)),
                code39_width_ratio=int(data.get("code39widthratio", 3)),
                code39_start_char=bool(data.get("code39startchar", True)),
                barcode_align=cast(Literal[0, 1, 2], int(data.get("barcodealign", 0))),
                pdf417_rows=int(data.get("pdf417_rows", 0)),
                pdf417_columns=int(data.get("pdf417_columns", 0)),
                pdf417_rows_auto=int(data.get("pdf417_rows_auto", 3)),
                pdf417_columns_auto=int(data.get("pdf417_columns_auto", 1)),
                datamatrix_shape=int(data.get("datamatrixShape", 0)),  # Note C# capitalization
                text_offset=float(data.get("textoffset", 0)),
                text_align=cast(
                    Literal[0, 1, 2, 3], int(data.get("textalign", 2))
                ),  # Different from TextElement's text_align
                text_font=data.get("textfont", "黑体"),
                text_font_size=float(data.get("fontsize", 10.0)),
                # Note: fontsize from the dict might be for the barcode text,
                # but BarcodeElement doesn't explicitly store it currently.
                # The DLL likely uses textfont for rendering the text below/above.
            )

        elif object_name.lower().startswith("rfiduhf"):  # Catches both UHF and HF as per comment
            # --- Create RFIDElement ---
            try:
                encoder_type = RFIDEncoderType(int(data.get("RFIDEncodertype", 0)))
            except ValueError:
                logger.warning(f"警告: 无效的 RFIDEncodertype 值 for {object_name}. 使用默认 UHF.")
                encoder_type = RFIDEncoderType.UHF

            data_block = None
            if encoder_type == RFIDEncoderType.UHF:
                try:
                    data_block = RFIDDataBlock(int(data.get("RFIDDatablock", 0)))
                except ValueError:
                    logger.warning(f"警告: 无效的 RFIDDatablock 值 for {object_name}. 使用默认 EPC.")
                    data_block = RFIDDataBlock.EPC

            try:
                data_type = RFIDDataType(int(data.get("RFIDDatatype", 0)))
            except ValueError:
                logger.warning(f"警告: 无效的 RFIDDatatype 值 for {object_name}. 使用默认 HEX.")
                data_type = RFIDDataType.HEX

            element = RFIDElement(
                object_name=object_name,
                data=obj_data,  # RFID data to write
                rfid_encoder_type=encoder_type,
                rfid_data_block=data_block,
                rfid_data_type=data_type,
                rfid_text_encoding=cast(Literal[0, 1], int(data.get("RFIDTextencoding", 0))),
                rfid_error_times=int(data.get("RFIDerrortimes", 2)),
                data_length_double_words=bool(data.get("Datalengthdoublewords", False)),
                data_alignment=cast(Literal[0, 1], int(data.get("DataAlignment", 0))),
                # Access Control (assuming keys exist if needed)
                rfid_epc_control=cast(Literal[0, 1, 2, 3, 4, 5, 6], int(data.get("RFIDepccontrol", 0))),
                rfid_user_control=cast(Literal[0, 1, 2, 3, 4, 5, 6], int(data.get("RFIDusercontrol", 0))),
                rfid_tid_control=cast(Literal[0, 1, 2, 3, 4, 5, 6], int(data.get("RFIDtidcontrol", 0))),
                rfid_access_pwd_control=cast(Literal[0, 1, 2, 3, 4, 5, 6], int(data.get("RFIDaccesspwdcontrol", 0))),
                rfid_kill_pwd_control=cast(Literal[0, 1, 2, 3, 4, 5, 6], int(data.get("RFIDkillpwdcontrol", 0))),
                rfid_access_new_pwd=data.get("RFIDaccessnewpwd", "00000000"),
                rfid_access_old_pwd=data.get("RFIDaccessoldpwd", "00000000"),
                rfid_use_kill_pwd=bool(data.get("RFIDusekillpwd", False)),
                rfid_kill_pwd=data.get("RFIDkillpwd", "00000000"),
                # HF specific
                hf_start_block=int(data.get("HFstartblock", 0)),
                hf_module_power=int(data.get("HFmodulepower", 0)),
                encrypt_14443a=bool(data.get("Encrypt14443A", False)),
                sector_14443a=int(data.get("Sector14443A", 1)),
                keyab_14443a=cast(Literal[0, 1, 2], int(data.get("KEYAB14443A", 0))),
                keya_new_pwd=data.get("KEYAnewpwd", ""),
                keya_old_pwd=data.get("KEYAoldpwd", "FFFFFFFFFFFF"),
                keyb_new_pwd=data.get("KEYBnewpwd", ""),
                keyb_old_pwd=data.get("KEYBoldpwd", "FFFFFFFFFFFF"),
                encrypt_14443a_control=bool(data.get("Encrypt14443AControl", False)),
                encrypt_14443a_control_value=data.get("Encrypt14443AControlvalue", "FF078069"),
                control_area_15693=cast(Literal[0, 1, 2], int(data.get("Controlarea15693", 0))),
                control_value_15693=data.get("Controlvalue15693", "00"),
            )

        elif object_name.lower().startswith("line"):
            # --- Create ShapeElement (Line) ---
            element = ShapeElement(
                object_name=object_name,
                shape_type="line",
                start_x=float(data.get("startXposition", x_pos)),  # Use specific or general
                start_y=float(data.get("startYposition", y_pos)),
                end_x=float(data.get("endXposition", x_pos + 10)),  # Default end
                end_y=float(data.get("endYposition", y_pos)),  # Default horizontal
                line_width=float(data.get("lineWidth", 0.4)),
            )
            # Add specific line/shape properties if they exist in dict
            if "lineDashStyle" in data:
                element.line_dash_style = cast(Literal[0, 1, 2, 3, 4], int(data["lineDashStyle"]))
            if "lineclass" in data:  # 1=horiz, 2=vert, 3=diag
                element.line_class = int(data["lineclass"])
            element.object_class = 1  # Explicitly set for shape

        elif object_name.lower().startswith("rectangle"):
            # --- Create ShapeElement (Rectangle) ---
            element = ShapeElement(
                object_name=object_name,
                shape_type="rectangle",
                start_x=float(data.get("startXposition", x_pos)),
                start_y=float(data.get("startYposition", y_pos)),
                end_x=float(data.get("endXposition", x_pos + 10)),  # Default end
                end_y=float(data.get("endYposition", y_pos + 5)),  # Default end
                line_width=float(data.get("lineWidth", 0.4)),
            )
            # Add specific rect/shape properties
            if "lineDashStyle" in data:
                element.line_dash_style = cast(Literal[0, 1, 2, 3, 4], int(data["lineDashStyle"]))
            if "fillRectangle" in data:
                element.fill_rectangle = bool(data["fillRectangle"])
            # rectangleclass seems to be always 0 (right-angle) in doc?
            element.rectangle_class = int(data.get("rectangleclass", 0))
            element.object_class = 2  # Explicitly set for shape

        elif object_name.lower().startswith("image"):
            # --- Create ImageElement ---
            img_data_raw = data.get("imagedata")
            img_data_bytes = None

            if isinstance(img_data_raw, str) and img_data_raw:
                # Attempt to decode if it looks like base64
                try:
                    # Simple check: is it likely base64?
                    if len(img_data_raw) % 4 == 0 and all(
                        c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=" for c in img_data_raw
                    ):
                        img_data_bytes = base64.b64decode(img_data_raw)
                    else:
                        logger.warning(
                            f"警告: 'imagedata' for {object_name} is a non-empty string but doesn't look like base64. Ignoring."
                        )
                except binascii.Error:
                    logger.warning(f"警告: Failed to decode base64 'imagedata' for {object_name}. Ignoring.")
                except Exception as decode_err:
                    logger.warning(f"警告: Error processing 'imagedata' for {object_name}: {decode_err}. Ignoring.")
            elif isinstance(img_data_raw, bytes):  # If already bytes
                img_data_bytes = img_data_raw

            if not img_data_bytes:
                raise ValueError(f"ImageElement '{object_name}' 缺少图像数据或图像数据无效.")

            fixed_width = float(data.get("imagefixedwidth", 0))
            fixed_height = float(data.get("imagefixedheight", 0))
            is_fixed = bool(data.get("imagefixedsize", fixed_width > 0 and fixed_height > 0))

            element = ImageElement(
                object_name=object_name,
                image_data=img_data_bytes,  # Must have data here
                x=x_pos,
                y=y_pos,
                fixed_width=fixed_width if is_fixed else None,
                fixed_height=fixed_height if is_fixed else None,
                aspect_ratio=bool(data.get("aspectRatio", True)),
                h_scale=int(data.get("hscale", 1)),
                v_scale=int(data.get("vscale", 1)),
            )
            element.image_fixed_size = is_fixed  # Ensure consistency

        else:
            raise ValueError(f"未知或不支持的 ObjectName 前缀: '{object_name}'.")

        # --- Common properties (apply if element was created) ---
        if element:
            element.direction = int(data.get("direction", 0))
            element.transparent = bool(data.get("transparent", True))  # Default to True
            # Add variables handling if needed/present in dict format
            # if "Variables" in data and isinstance(data["Variables"], list):
            #    element.variables = data["Variables"] # Adjust structure as needed

        return element


class TextElement(LabelElement):
    """文本元素"""

    def __init__(
        self,
        object_name: str,
        data: str,
        x: float = 3.0,
        y: float = 3.0,
        font_name: str = "黑体",
        font_size: float = 10.0,
        font_style: Literal[0, 1, 2, 3] = 0,  # 0:常规, 1:粗体, 2:斜体, 3:粗斜体
        text_align: Literal[0, 1, 2] = 0,  # 文字的对齐方式，0为左对齐，1为居中，2为右对齐
        text_valign: Literal[0, 1, 2] = 0,  # 文字的对齐方式，0为顶边对齐，1为垂直居中，2为底边对齐
        is_multiline: bool = False,
        width: Optional[float] = None,  # 多行文本宽度 段落文本的宽度，单位mm
        width_handling: Literal[
            0, 1, 2
        ] = 0,  # 段落文本超出指定宽度后处理，0为自动换行，1为自动压扁字体，2为自动缩小字体
        black_background: bool = False,  # 是否黑底白字
        char_gap: float = 0,  # 字符间距，单位mm
        char_h_zoom: float = 1,  # 字符横向缩放倍数，0.3~2
        line_gap_index: Literal[0, 1, 2, 3] = 0,  # 段落文本的行间距，0为单倍，1为一倍半，2为双倍，3为自定义
        line_gap: float = 0,  # 自定义的行间距
        circular_radius: float = 2.0,  # 圆形环绕文字的圆形半径
        text_radian: int = 360,  # 圆形环绕文字的文本弧度
        text_start_angle: int = 0,  # 圆形环绕文字的起始角度
        rewinding_direction: Literal[0, 1] = 0,  # 圆形环绕文字的回绕方向，0 顺时针，1 逆时针
        literal_direction: Literal[0, 1] = 0,  # 圆形环绕文字的文字方向，0 向外，1 向内
    ):
        super().__init__(object_name, x, y, data)
        self.element_type = "text"
        self.font_name = font_name
        self.font_size = font_size
        self.font_style = font_style
        self.text_align = text_align
        self.text_valign = text_valign
        self.is_multiline = is_multiline
        self.width = width
        self.width_handling = width_handling
        self.black_background = black_background
        self.char_gap = char_gap
        self.char_h_zoom = char_h_zoom
        self.text_type = 0 if not is_multiline else 1  # 文本类型，0为单行文本，1为段落文本，2为圆形环绕文字
        self.text_text_align = text_align
        self.text_text_valign = text_valign
        self.text_width = width if width else 30
        self.text_width_beyound = width_handling
        self.line_gap_index = line_gap_index
        self.line_gap = line_gap
        self.circular_radius = circular_radius
        self.text_radian = text_radian
        self.text_start_angle = text_start_angle
        self.rewinding_direction = rewinding_direction
        self.literal_direction = literal_direction


class BarcodeElement(LabelElement):
    """条码/二维码元素"""

    def __init__(
        self,
        object_name: str,
        data: str,
        barcode_type: Union[BarcodeType, str],
        x: float = 3.0,
        y: float = 3.0,
        scale: float = 3.0,  # 对于一维码是宽度比例，二维码是模块大小
        height: Optional[float] = None,  # 仅一维码需要
        text_position: Literal[0, 1, 2] = 0,  # 0:下方, 1:上方, 2:不显示 (一维码)
        direction: Literal[0, 1, 2, 3] = 0,  # 0:0度, 1:90度, 2:180度, 3:270度
        error_correction: Literal[0, 1, 2, 3] = 0,  # QR码的纠错等级，0:L,1:M,2:Q,3:H
        char_encoding: Literal[0, 1] = 0,  # QR码的字符编码,0为UTF-8，1为GB2312
        qr_version: int = 0,  # QR符号版本，1~40，数字越大包含字符越多,0为自动
        code39_width_ratio: int = 3,  # Code39码的条宽比
        code39_start_char: bool = True,  # Code39码是否包含起始符*
        barcode_align: Literal[0, 1, 2] = 0,  # 条码的对齐方式，0为左对齐，1为居中对齐，2为右对齐
        pdf417_rows: int = 0,  # PDF417条码的行数，即层数，0为自动
        pdf417_columns: int = 0,  # PDF417条码的列数，即数据的块数，左右两个标识块不算在内，0为自动
        pdf417_rows_auto: int = 3,  # PDF417条码的行数设置为自动时，得到的行数，最小为3
        pdf417_columns_auto: int = 1,  # PDF417条码的列数设置为自动时，得到的列数，最小为1
        datamatrix_shape: int = 0,  # DataMatrix的形状，0为自动，1为正方形，2为矩形
        text_offset: float = 0,  # 文字和条码的距离，单位mm
        text_align: Literal[0, 1, 2, 3] = 2,  # 文字相对于条码的对齐方式，0为左侧、1为右侧、2为居中、3为撑满
        text_font: str = "黑体",  # 字体名称
        text_font_size: float = 10.0,
    ):
        super().__init__(object_name, x, y, data)
        self.element_type = "barcode"
        # 允许传入枚举成员或字符串
        self.barcode_type = barcode_type.value if isinstance(barcode_type, Enum) else barcode_type
        self.scale = scale
        self.height = height
        self.text_position = text_position
        self.direction = direction
        self.error_correction = error_correction
        self.char_encoding = char_encoding
        self.qr_version = qr_version
        self.code39_width_ratio = code39_width_ratio
        self.code39_start_char = code39_start_char
        self.barcode_align = barcode_align
        self.pdf417_rows = pdf417_rows
        self.pdf417_columns = pdf417_columns
        self.pdf417_rows_auto = pdf417_rows_auto
        self.pdf417_columns_auto = pdf417_columns_auto
        self.datamatrix_shape = datamatrix_shape
        self.text_offset = text_offset
        self.text_align = text_align
        self.text_font = text_font
        self.text_font_size = text_font_size


class ImageElement(LabelElement):
    """图像元素"""

    def __init__(
        self,
        object_name: str,
        image_path: Optional[str | Path] = None,  # 本地文件路径
        image_data: Optional[bytes] = None,  # 或者直接提供 bytes
        x: float = 3.0,
        y: float = 3.0,
        fixed_width: Optional[float] = None,
        fixed_height: Optional[float] = None,
        aspect_ratio: bool = True,  # 图片是否保持长宽比，默认是
        h_scale: int = 1,  # 横向缩放率百分比
        v_scale: int = 1,  # 竖向缩放率百分比
    ):
        super().__init__(object_name, x, y)
        self.element_type = "image"
        if image_path and image_data:
            raise ValueError("Provide either image_path or image_data, not both.")
        if not image_path and not image_data:
            raise ValueError("Must provide either image_path or image_data.")

        if image_path:
            # 在 .NET 端加载图片可能更可靠，尤其是在处理路径时
            # 或者在这里读取并传递 bytes
            try:
                with open(image_path, "rb") as f:
                    self.image_data = f.read()
            except Exception as e:
                raise IOError(f"Failed to read image file {image_path}: {e}")
        else:
            self.image_data = image_data

        self.fixed_width = fixed_width
        self.fixed_height = fixed_height
        self.aspect_ratio = aspect_ratio
        self.h_scale = h_scale
        self.v_scale = v_scale
        self.image_fixed_size = fixed_width is not None and fixed_height is not None  # 是否固定尺寸
        self.image_fixed_width = fixed_width if fixed_width else 0  # 图片固定宽度，单位是mm
        self.image_fixed_height = fixed_height if fixed_height else 0  # 图片固定高度，单位是mm


class RFIDElement(LabelElement):
    """RFID 写入元素"""

    def __init__(
        self,
        object_name: str,
        data: str,
        # UHF
        rfid_encoder_type: RFIDEncoderType = RFIDEncoderType.UHF,
        rfid_data_block: Optional[RFIDDataBlock] = None,  # UHF specific
        rfid_data_type: RFIDDataType = RFIDDataType.HEX,
        rfid_text_encoding: Literal[0, 1] = 0,  # 文本编码：0为ASCII，1为UTF-8
        rfid_error_times: int = 2,  # 重试次数
        data_length_double_words: bool = False,  # 强制以4个字节为单位写入
        data_alignment: Literal[0, 1] = 0,  # 数据对齐方式，0为后端补零，1为前端补零
        # 访问控制
        rfid_epc_control: Literal[0, 1, 2, 3, 4, 5, 6] = 0,  # EPC区访问控制
        rfid_user_control: Literal[0, 1, 2, 3, 4, 5, 6] = 0,  # USER区访问控制
        rfid_tid_control: Literal[0, 1, 2, 3, 4, 5, 6] = 0,  # TID区访问控制
        rfid_access_pwd_control: Literal[0, 1, 2, 3, 4, 5, 6] = 0,  # 访问密码区访问控制
        rfid_kill_pwd_control: Literal[0, 1, 2, 3, 4, 5, 6] = 0,  # 灭活密码区访问控制
        # 以上访问控制的值：0为开放，1为锁定，2为解除锁定，3为永久锁定，4为永久解除锁定
        # 5为先解除锁定再重新锁定，6为先解除锁定再重新永久锁定
        rfid_access_new_pwd: str = "00000000",  # 访问密码新密码
        rfid_access_old_pwd: str = "00000000",  # 访问密码旧密码
        rfid_use_kill_pwd: bool = False,  # 是否使用灭活密码
        rfid_kill_pwd: str = "00000000",  # 灭活密码
        # HF
        hf_start_block: int = 0,  # HF specific 14443A=1, NFC=4, 15693=0
        hf_module_power: int = 0,  # 高频模块功率，0 为自动
        encrypt_14443a: bool = False,  # 是否要加密14443A标签
        sector_14443a: int = 1,  # 需要加密的1443A的扇区
        keyab_14443a: Literal[0, 1, 2] = 0,  # 需要加密KEYA或KEYB，0为KEYA，1为KEYB，2为两个都加密
        keya_new_pwd: str = "",  # KEYA新密码
        keya_old_pwd: str = "FFFFFFFFFFFF",  # KEYA旧密码
        keyb_new_pwd: str = "",  # KEYB新密码
        keyb_old_pwd: str = "FFFFFFFFFFFF",  # KEYB旧密码
        encrypt_14443a_control: bool = False,  # 是否要设置14443A的控制字
        encrypt_14443a_control_value: str = "FF078069",  # 设置的14443A的控制字
        control_area_15693: Literal[0, 1, 2] = 0,  # 0为不设置，1为AFI，2为DSFID
        control_value_15693: str = "00",  # 设置的值，默认是00
    ):
        super().__init__(object_name, data=data)  # 位置对于 RFID 无意义
        self.element_type = "rfid"
        self.encoder_type = rfid_encoder_type
        self.data_block = rfid_data_block
        self.data_type = rfid_data_type
        self.hf_start_block = hf_start_block
        # UHF相关
        self.rfid_encoder_type = rfid_encoder_type.value  # 0为UHF，1为HF 15693，2为HF 14443，3为NFC
        self.rfid_data_block = rfid_data_block.value if rfid_data_block else 0  # 写入数据区：0为EPC，1为USER
        self.rfid_data_type = rfid_data_type.value  # 写入的数据类型：0为文本，1为16进制
        self.rfid_text_encoding = rfid_text_encoding
        self.data_alignment = data_alignment
        self.rfid_error_times = rfid_error_times
        self.data_length_double_words = data_length_double_words
        self.rfid_epc_control = rfid_epc_control
        self.rfid_user_control = rfid_user_control
        self.rfid_tid_control = rfid_tid_control
        self.rfid_access_pwd_control = rfid_access_pwd_control
        self.rfid_kill_pwd_control = rfid_kill_pwd_control
        self.rfid_access_new_pwd = rfid_access_new_pwd
        self.rfid_access_old_pwd = rfid_access_old_pwd
        self.rfid_use_kill_pwd = rfid_use_kill_pwd
        self.rfid_kill_pwd = rfid_kill_pwd

        # HF相关
        self.hf_start_block = hf_start_block  # 高频，要写的块的起点地址
        self.hf_module_power = hf_module_power  # 高频模块功率
        self.encrypt_14443a = encrypt_14443a  # 是否要加密14443A标签
        self.sector_14443a = sector_14443a  # 需要加密的1443A的扇区
        self.keyab_14443a = keyab_14443a  # 需要加密KEYA或KEYB，0为KEYA，1为KEYB，2为两个都加密
        self.keya_new_pwd = keya_new_pwd  # KEYA新密码
        self.keya_old_pwd = keya_old_pwd  # KEYA旧密码
        self.keyb_new_pwd = keyb_new_pwd  # KEYB新密码
        self.keyb_old_pwd = keyb_old_pwd  # KEYB旧密码
        self.encrypt_14443a_control = encrypt_14443a_control  # 是否要设置14443A的控制字
        self.encrypt_14443a_control_value = encrypt_14443a_control_value  # 设置的14443A的控制字
        self.control_area_15693 = control_area_15693  # 0为不设置，1为AFI，2为DSFID
        self.control_value_15693 = control_value_15693  # 设置的值，默认是00


class ShapeElement(LabelElement):
    """形状元素 (直线/矩形)"""

    def __init__(
        self,
        object_name: str,
        shape_type: Literal["line", "rectangle"],  # "line" or "rectangle"
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        line_width: float = 0.4,
        fill_rectangle: bool = False,
        line_dash_style: Literal[
            0, 1, 2, 3, 4
        ] = 0,  # 条线样式，0为实线，1为破折虚线，2为破折点虚线，3为破折点点虚线，4为点虚线
    ):
        super().__init__(object_name, x=start_x, y=start_y)  # 使用起始点作为位置
        self.element_type = "shape"
        if shape_type not in ["line", "rectangle"]:
            raise ValueError("shape_type must be 'line' or 'rectangle'")
        self.shape_type = shape_type
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.line_width = line_width
        self.start_x_position = start_x  # 直线和矩形在标签上起始点的位置，单位是mm
        self.start_y_position = start_y  # 直线和矩形在标签上起始点的位置，单位是mm
        self.end_x_position = end_x  # 直线和矩形在标签上终止点的位置，单位是mm
        self.end_y_position = end_y  # 直线和矩形在标签上终止点的位置，单位是mm
        self.line_dash_style = line_dash_style  # 条线样式，0为实线，1为破折虚线，2为破折点虚线，3为破折点点虚线，4为点虚线  # 条线样式，0为实线，1为破折虚线，2为破折点虚线，3为破折点点虚线，4为点虚线
        self.fill_rectangle = fill_rectangle  # 是否填充矩形
        self.line_class = 1 if shape_type == "line" else 0  # 直线的类别，1为横线，2为竖线，3为斜线
        self.rectangle_class = 0 if shape_type == "rectangle" else None  # 矩形的类别，0为直角矩形
        self.object_class = 1 if shape_type == "line" else 2  # 对象类型，1是线，2是矩形


LabelElementType = Union[TextElement, BarcodeElement, ImageElement, RFIDElement, ShapeElement]

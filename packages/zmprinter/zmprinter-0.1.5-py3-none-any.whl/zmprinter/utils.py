import os
import logging
from typing import Optional

# 默认日志格式
DEFAULT_LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
DEFAULT_LOG_LEVEL = "INFO"

# 创建一个全局的logger字典，用于跨文件共享logger实例
_loggers = {}


def get_logger(
    name: str = "zmprinter", log_level: Optional[str] = None, log_format: Optional[str] = None
) -> logging.Logger:
    """
    获取或创建一个名为name的logger实例。

    :param name: logger名称，默认为'zmprinter'
    :param log_level: 日志级别，默认从环境变量ZMPRINTER_LOG_LEVEL获取，如未设置则为INFO
    :param log_format: 日志格式，默认从环境变量ZMPRINTER_LOG_FORMAT获取，如未设置则使用默认格式
    :return: 配置好的Logger实例
    """
    # 如果已经创建过该名称的logger，则直接返回
    if name in _loggers:
        return _loggers[name]

    # 创建新的logger
    logger = logging.getLogger(name)

    # 防止日志重复：如果此logger有父级并且传播enabled，则不添加处理器
    if name != "zmprinter" and "." in name and logger.propagate:
        _loggers[name] = logger
        return logger

    # 设置日志级别
    if log_level is None:
        log_level = os.getenv("ZMPRINTER_LOG_LEVEL", DEFAULT_LOG_LEVEL)

    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)

    # 设置日志格式
    if log_format is None:
        log_format = os.getenv("ZMPRINTER_LOG_FORMAT", DEFAULT_LOG_FORMAT)

    # 检查logger是否已有处理器，如果没有，添加一个控制台处理器
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(log_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # 保存logger实例以便重用
    _loggers[name] = logger

    return logger


def setup_file_logging(
    filename: str,
    name: str = "zmprinter",
    log_level: Optional[str] = None,
    log_format: Optional[str] = None,
    mode: str = "a",
) -> logging.Logger:
    """
    设置文件日志记录。

    :param filename: 日志文件路径
    :param name: logger名称，默认为'zmprinter'
    :param log_level: 日志级别，默认从环境变量获取
    :param log_format: 日志格式，默认从环境变量获取
    :param mode: 文件打开模式，默认为'a'（追加）
    :return: 配置好的Logger实例
    """
    logger = get_logger(name, log_level, log_format)

    # 检查是否已有相同路径的文件处理器
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler) and getattr(handler, "baseFilename", None) == os.path.abspath(
            filename
        ):
            return logger

    # 添加文件处理器
    file_handler = logging.FileHandler(filename, mode=mode)

    # 设置日志格式
    if log_format is None:
        log_format = os.getenv("ZMPRINTER_LOG_FORMAT", DEFAULT_LOG_FORMAT)

    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)

    # 设置日志级别
    if log_level is None:
        log_level = os.getenv("ZMPRINTER_LOG_LEVEL", DEFAULT_LOG_LEVEL)

    level = getattr(logging, log_level.upper(), logging.INFO)
    file_handler.setLevel(level)

    # 添加处理器到logger
    logger.addHandler(file_handler)

    return logger

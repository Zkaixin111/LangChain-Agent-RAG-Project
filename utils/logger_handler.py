import logging
import os
from datetime import datetime

from utils.path_tool import get_abs_path

# 日志保存的根目录
LOG_ROOT = get_abs_path('logs')

# 创建日志目录，确保日志目录存在
os.makedirs(LOG_ROOT, exist_ok=True)

# 日志的格式配置
# 默认日志格式：时间 级别 [文件名:行号] 消息
DEFAULT_LOG_FORMAT = logging.Formatter(
    fmt='%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 详细日志格式（包含线程、进程信息）
DETAILED_LOG_FORMAT = logging.Formatter(
    fmt='%(asctime)s %(levelname)s [%(threadName)s:%(processName)s] [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 记录已初始化的logger，避免重复添加handler
_initialized_loggers = set()


def get_logger(name: str = "agent", log_to_file: bool = True, log_level: int = logging.DEBUG) -> logging.Logger:
    """
    获取配置好的logger实例

    Args:
        name: logger名称，通常使用 __name__
        log_to_file: 是否同时输出到文件，默认为True
        log_level: 日志级别，默认为DEBUG

    Returns:
        配置好的Logger对象
    """
    # 获取指定名称的日志记录器实例
    logger = logging.getLogger(name)

    # 如果已经初始化过，直接返回
    if name in _initialized_loggers:
        return logger

    # 设置日志记录器的最低日志级别
    logger.setLevel(log_level)

    # 关键：禁止日志传播到父logger，避免重复打印
    logger.propagate = False

    # 控制台handler - 显示INFO及以上级别的日志
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(console_handler)

    # 文件handler - 记录所有级别的日志
    if log_to_file:
        # 按日期生成日志文件名
        log_date = datetime.now().strftime('%Y%m%d')
        log_filename = f'{name}_{log_date}.log'
        log_filepath = os.path.join(LOG_ROOT, log_filename)

        # 文件Handler - 使用追加模式
        file_handler = logging.FileHandler(log_filepath, encoding='utf-8', mode='a')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(DEFAULT_LOG_FORMAT)
        logger.addHandler(file_handler)

    # 标记为已初始化
    _initialized_loggers.add(name)

    return logger


logger = get_logger()

if __name__ == '__main__':
    # 给出测试
    logger = get_logger(__name__)
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')

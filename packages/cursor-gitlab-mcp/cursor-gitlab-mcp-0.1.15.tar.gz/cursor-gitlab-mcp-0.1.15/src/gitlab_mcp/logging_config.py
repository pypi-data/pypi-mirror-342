import os
import logging
from pathlib import Path
import sys

def setup_logging():
    """
    设置日志配置
    """
    # 配置日志目录
    if sys.platform == 'win32':
        log_dir = os.path.join(os.getenv('APPDATA'), 'cursor-gitlab-mcp')
    else:
        log_dir = os.path.join(str(Path.home()), '.local', 'share', 'cursor-gitlab-mcp')
    
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'gitlab_mcp.log')

    # 配置日志格式
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )

    # 文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # 获取根日志记录器
    logger = logging.getLogger('gitlab_mcp')
    logger.setLevel(logging.DEBUG)
    
    # 清除现有的处理器
    logger.handlers.clear()
    
    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger 
"""
GitLab MCP主程序
"""

import os
import sys
import logging
import argparse
from typing import Optional
from .server import mcp_command
from .utils import setup_logging

logger = logging.getLogger('gitlab_mcp')

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='GitLab MCP命令行工具')
    parser.add_argument('command', help='要执行的命令')
    parser.add_argument('--log-path', help='自定义日志文件路径')
    return parser.parse_args()

def main():
    """主函数"""
    try:
        # 解析命令行参数
        args = parse_args()
        
        # 设置日志
        log_path = args.log_path
        setup_logging(log_path)
        logger.info("GitLab MCP启动")
        
        # 执行命令
        logger.info(f"执行命令: {args.command}")
        result = mcp_command(args.command, log_path=log_path)
        
        if result:
            logger.info("命令执行成功")
            print(result)
        else:
            logger.warning("命令执行失败")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 
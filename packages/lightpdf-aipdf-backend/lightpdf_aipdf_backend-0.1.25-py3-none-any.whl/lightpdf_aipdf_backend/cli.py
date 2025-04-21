"""
CLI命令入口
"""
import asyncio
import sys
from .main import main

def run_server():
    """运行API服务器的命令行入口点"""
    # 获取命令行参数中的端口，如果提供的话
    port = 3300  # 默认端口
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"错误：端口必须是整数，将使用默认端口 {port}")
    
    asyncio.run(main(port=port)) 
"""
后端应用主入口模块
"""
import asyncio
import sys
from .main import main

if __name__ == "__main__":
    # 获取命令行参数中的端口，如果提供的话
    port = 3300  # 默认端口
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"错误：端口必须是整数，将使用默认端口 {port}")
    
    asyncio.run(main(port=port)) 
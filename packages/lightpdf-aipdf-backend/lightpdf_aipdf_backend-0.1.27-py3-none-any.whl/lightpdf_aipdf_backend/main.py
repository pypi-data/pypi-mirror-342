import os
import asyncio
import sys
import uvicorn
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from .state import set_mcp_session, get_openai_client
from .app import app
from .tools import get_tools

async def main(port=3300):
    """应用主入口"""
    # 打印版本号
    try:
        import importlib.metadata
        version = importlib.metadata.version("lightpdf-aipdf-backend")
        print(f"LightPDF AI-PDF Backend v{version}", file=sys.stderr)
    except Exception as e:
        print("LightPDF AI-PDF Backend (版本信息获取失败)", file=sys.stderr)
    
    # 初始化 OpenAI 客户端 - 只需调用get_openai_client即可
    get_openai_client()
    
    # 准备 MCP 服务参数
    server_params = StdioServerParameters(
        command="uvx",
        args=["lightpdf-aipdf-mcp@latest"],
        # args=["-n", "../../../mcp_server/dist/lightpdf_aipdf_mcp-0.0.1-py3-none-any.whl"],
        env={
            "API_KEY": os.getenv("API_KEY"),
        }
    )
    
    # 启动 MCP 会话
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # 设置全局 MCP 会话
            set_mcp_session(session)

            tools = await get_tools()
            print(tools)
            
            print(f"正在启动服务，监听端口: {port}")
            # 启动 FastAPI 服务器
            config = uvicorn.Config(app, host="0.0.0.0", port=port)
            server = uvicorn.Server(config)
            await server.serve()

# 确保与原始 main 函数相同
if __name__ == "__main__":
    asyncio.run(main()) 
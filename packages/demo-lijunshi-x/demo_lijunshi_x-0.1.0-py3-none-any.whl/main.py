from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP()

@mcp.tool()
def get_nowtime() -> str:
    """获取当前时间（北京时间）"""
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    mcp.run(transport='stdio')  # 启用调试模式
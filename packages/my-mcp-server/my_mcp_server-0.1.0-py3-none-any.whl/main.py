from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务
mcp = FastMCP("HelloWorld")

@mcp.tool()
def say_hello(name: str = "世界") -> str:
    return f"你好，{name}！这是来自 MCP 的问候 👋"

if __name__ == "__main__":
    mcp.run(transport="stdio")
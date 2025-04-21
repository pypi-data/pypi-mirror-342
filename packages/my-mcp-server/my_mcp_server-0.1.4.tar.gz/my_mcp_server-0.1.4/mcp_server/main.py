from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务
mcp = FastMCP("HelloWorld")

@mcp.tool()
def say_hello(name: str = "世界") -> str:
    return f"你好，{name}！这是来自 MCP 的问候 👋"

def main():  # 添加 main 函数用于入口点
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
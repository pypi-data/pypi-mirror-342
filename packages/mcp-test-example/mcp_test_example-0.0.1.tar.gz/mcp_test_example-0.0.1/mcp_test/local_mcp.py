from mcp.server.fastmcp import FastMCP
import os


mcp = FastMCP("local-server", host="127.0.0.1", port="6277", debug=True)  # 初始化服务器

@mcp.tool()
def count_letter_r(text: str) -> int:
    """统计字符串中字母'r'的出现次数"""
    return text.lower().count('r')

@mcp.tool()
def list_files(directory: str) -> list:
    """列出指定目录下的所有文件（支持跨平台）"""
    return os.listdir(os.path.expanduser(directory))


if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run(transport='stdio')




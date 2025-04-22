import asyncio
import json
from baidu_search_playwright_server import BaiduSearchPlaywrightServer
async def test_playwright_search():
    """测试百度搜索服务器的基本功能"""
    print("初始化百度搜索服务器...")
    search_server = BaiduSearchPlaywrightServer()
    search_results = await search_server.mcp.call_tool("baidu_search",{"query":query, "page":1})
    print(search_results)


if __name__ == "__main__":
    asyncio.run(test_playwright_search())
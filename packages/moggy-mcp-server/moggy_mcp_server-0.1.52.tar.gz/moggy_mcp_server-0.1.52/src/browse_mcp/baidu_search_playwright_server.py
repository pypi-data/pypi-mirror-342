import base64
import json
from mcp.server.fastmcp import FastMCP, Context
from mcp.types import TextContent, ImageContent
from playwright.async_api import Page
from browse_mcp.browse_manager import BrowserManager
from pydantic import BaseModel, Field
from browse_mcp.tools.file_tools import FileTools
from autogen_ext.agents.web_surfer.playwright_controller import PlaywrightController
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

class SearchResult(BaseModel):
    """百度搜索结果的数据模型"""
    title: str = Field(description="搜索结果的标题")
    url: str = Field(description="搜索结果的URL链接")
    snippet: str = Field(description="搜索结果的简介摘要")
    source: Optional[str] = Field(None, description="来源网站")
    time: Optional[str] = Field(None, description="发布时间（如果有）")

class BaiduSearchPlaywrightServer(FastMCP):
    """基于百度引擎的MCP搜索服务器"""
    
    def __init__(self, server_name="baidu-search-server"):
        super().__init__(server_name)
        self.mcp = self
        self.browser_manager = BrowserManager()
        self.file_tools = FileTools()
        self.search_results_cache = {}
        self.current_page = 1
        self.current_query = ""
        self.total_pages = 1
        
        self.register_tools()
        self.register_resources()
        self.register_prompts()

    def register_tools(self):
        @self.mcp.tool(description="在百度上搜索并获取结果")
        async def baidu_search(query: str, page: int = 1):
            """在百度上执行搜索查询并返回结果"""
            try:
                self.current_query = query
                self.current_page = page
                
                # 构建百度搜索URL
                search_url = f"https://www.baidu.com/s?wd={query}&pn={(page-1)*10}"
                
                # 导航到搜索页面
                browser_page: Page = await self.browser_manager.ensure_browser()
                await browser_page.goto(url=search_url, wait_until="domcontentloaded", timeout=30000)
                
                # 等待搜索结果加载
                await browser_page.wait_for_selector(".result", timeout=5000)
                
                # 提取搜索结果
                results = await self._extract_search_results(browser_page)
                
                # 提取分页信息
                total_pages = await self._extract_pagination_info(browser_page)
                self.total_pages = total_pages
                
                # 缓存结果
                cache_key = f"{query}_{page}"
                self.search_results_cache[cache_key] = results
                
                # 构建返回信息
                return {
                    "query": query,
                    "page": page,
                    "total_pages": total_pages,
                    "results": [result.dict() for result in results],
                    "result_count": len(results)
                }
            except Exception as e:
                raise ValueError(f"搜索失败: {e}")
        
        @self.mcp.tool(description="获取下一页搜索结果")
        async def next_page():
            """获取当前搜索查询的下一页结果"""
            if not self.current_query:
                return "请先执行搜索查询"
                
            if self.current_page >= self.total_pages:
                return "已经是最后一页"
                
            next_page = self.current_page + 1
            return await baidu_search(self.current_query, next_page)
        
        @self.mcp.tool(description="获取上一页搜索结果")
        async def previous_page():
            """获取当前搜索查询的上一页结果"""
            if not self.current_query:
                return "请先执行搜索查询"
                
            if self.current_page <= 1:
                return "已经是第一页"
                
            prev_page = self.current_page - 1
            return await baidu_search(self.current_query, prev_page)
        
        @self.mcp.tool(description="获取搜索结果的详细信息")
        async def get_result_details(result_index: int):
            """获取特定搜索结果的详细信息"""
            if not self.current_query:
                return "请先执行搜索查询"
                
            cache_key = f"{self.current_query}_{self.current_page}"
            if cache_key not in self.search_results_cache:
                return "没有找到缓存的搜索结果，请重新搜索"
                
            results = self.search_results_cache[cache_key]
            if result_index < 0 or result_index >= len(results):
                return f"结果索引超出范围，有效范围: 0-{len(results)-1}"
                
            result = results[result_index]
            
            # 导航到结果页面获取更多信息
            browser_page: Page = await self.browser_manager.ensure_browser()
            await browser_page.goto(url=result.url, wait_until="domcontentloaded", timeout=30000)
            
            # 获取页面标题和内容
            page_title = await browser_page.title()
            playwright_controller = PlaywrightController()
            page_content = await playwright_controller.get_page_markdown(browser_page)
            
            return {
                "title": page_title,
                "url": result.url,
                "original_snippet": result.snippet,
                "content_preview": page_content[:1000] + "..." if len(page_content) > 1000 else page_content
            }
        
        @self.mcp.tool(description="获取相关搜索建议")
        async def get_related_searches():
            """获取与当前搜索相关的搜索建议"""
            if not self.current_query:
                return "请先执行搜索查询"
                
            browser_page: Page = await self.browser_manager.ensure_browser()
            
            # 尝试提取相关搜索
            try:
                related_searches = await browser_page.evaluate("""
                    () => {
                        const relatedElements = document.querySelectorAll('.rs-link');
                        return Array.from(relatedElements).map(el => el.textContent.trim());
                    }
                """)
                return related_searches if related_searches else "未找到相关搜索建议"
            except Exception as e:
                return f"获取相关搜索建议失败: {e}"
        
        @self.mcp.tool(description="获取当前页面的截图")
        async def get_search_screenshot():
            """获取当前搜索结果页面的截图"""
            try:
                browser_page: Page = await self.browser_manager.ensure_browser()
                screenshot = await browser_page.screenshot(type="png")
                screenshot_base64 = base64.b64encode(screenshot).decode("utf-8")
                
                screenshot_name = f"search_{self.current_query}_{self.current_page}"
                self.screenshots[screenshot_name] = screenshot_base64
                
                return [
                    TextContent(type="text", text=f"搜索结果截图已生成"),
                    ImageContent(type="image", data=screenshot_base64, mimeType="image/png")
                ]
            except Exception as e:
                raise ValueError(f"截图失败: {e}")
    
    async def _extract_search_results(self, page: Page) -> List[SearchResult]:
        """从百度搜索页面提取搜索结果"""
        results = []
        
        # 使用JavaScript提取搜索结果
        raw_results = await page.evaluate("""
            () => {
                const resultElements = document.querySelectorAll('.result');
                return Array.from(resultElements).map(el => {
                    // 提取标题和URL
                    const titleEl = el.querySelector('.t a, .c-title a');
                    const title = titleEl ? titleEl.textContent.trim() : '';
                    const url = titleEl ? titleEl.href : '';
                    
                    // 提取摘要
                    const snippetEl = el.querySelector('.c-abstract, .content-abstract');
                    const snippet = snippetEl ? snippetEl.textContent.trim() : '';
                    
                    // 提取来源和时间（如果有）
                    const sourceEl = el.querySelector('.c-author, .c-color-gray');
                    const source = sourceEl ? sourceEl.textContent.trim() : null;
                    
                    // 提取时间（通常包含在来源信息中）
                    let time = null;
                    if (source) {
                        const timeMatch = source.match(/\d{4}年\d{1,2}月\d{1,2}日|\d{1,2}天前|\d{1,2}小时前/);
                        time = timeMatch ? timeMatch[0] : null;
                    }
                    
                    return { title, url, snippet, source, time };
                });
            }
        """)
        
        # 将原始结果转换为SearchResult对象
        for item in raw_results:
            if item['title'] and item['url']:
                results.append(SearchResult(
                    title=item['title'],
                    url=item['url'],
                    snippet=item['snippet'] if item['snippet'] else "无摘要",
                    source=item['source'],
                    time=item['time']
                ))
        
        return results
    
    async def _extract_pagination_info(self, page: Page) -> int:
        """提取分页信息"""
        try:
            # 尝试获取总页数
            total_pages = await page.evaluate("""
                () => {
                    const pageInfo = document.querySelector('.page-inner');
                    if (pageInfo) {
                        const lastPage = pageInfo.querySelector('a:last-of-type');
                        if (lastPage && lastPage.textContent) {
                            const pageNum = parseInt(lastPage.textContent.trim());
                            return isNaN(pageNum) ? 1 : pageNum;
                        }
                    }
                    return 1; // 默认为1页
                }
            """)
            return total_pages
        except Exception:
            return 1  # 如果无法提取，默认为1页
    
    def register_resources(self):
        @self.mcp.resource("screenshot://{name}")
        async def get_screenshot(name: str):
            """获取指定名称的截图"""
            screenshot_base64 = self.screenshots.get(name)
            if screenshot_base64:
                return ImageContent(
                    type="image",
                    data=screenshot_base64,
                    mimeType="image/png",
                    uri=f"screenshot://{name}"
                )
            else:
                raise ValueError(f"截图 {name} 未找到")
    
    def register_prompts(self):
        @self.mcp.prompt()
        async def search_help():
            return """
            # 百度搜索助手使用指南
            
            本服务提供以下功能：
            
            1. **基本搜索**：使用`baidu_search`工具在百度上执行搜索查询
            2. **分页浏览**：使用`next_page`和`previous_page`工具浏览搜索结果的不同页面
            3. **详细信息**：使用`get_result_details`工具获取特定搜索结果的详细信息
            4. **相关搜索**：使用`get_related_searches`工具获取相关搜索建议
            5. **页面截图**：使用`get_search_screenshot`工具获取当前搜索结果页面的截图
            
            示例：
            ```
            # 执行搜索
            baidu_search("人工智能最新进展")
            
            # 获取下一页结果
            next_page()
            
            # 获取第一个结果的详细信息
            get_result_details(0)
            ```
            """

app = BaiduSearchPlaywrightServer()

def main():
    app.run()

print("BaiduSearchServer is running...")
import logging
import json
from pydantic import BaseModel, Field
from enum import Enum
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from spider_rs import Website


class SpiderArgs(BaseModel):
    url: str = Field(description="The url to crawl/scrape")
    headers: dict[str, str] | None = Field(description="Additional headers to pass along crawling/scraping requests")
    user_agent: str | None = Field(description="User agent for the crawl/scrape request")
    depth: int | None = Field(description="Crawl/Scrape depth limit. Don't use if you want unlimited crawl/scrape depth")
    blacklist: list[str] | None = Field(description="Regex that blacklists urls from the crawl/scrape process")
    whitelist: list[str] | None = Field(description="Regex that whitelists urls from the crawl/scrape process")
    respect_robots_txt: bool | None = Field(description="Whether to respect robots.txt file")
    accept_invalid_certs: bool | None = Field(description="Accept invalid certificates - should be used as last resort")

    def build_website(self, is_scrape: bool) -> Website:
        website = Website(self.url)
    
        if self.headers:
            website = website.with_headers(self.headers)
    
        if self.user_agent:
            website = website.with_user_agent(self.user_agent)

        if self.depth:
            website = website.with_depth(self.depth)
    
        if self.blacklist:
            website = website.with_blacklist_url(self.blacklist)
    
        if self.whitelist:
            website = website.with_whitelist_url(self.whitelist)
    
        if self.respect_robots_txt is not None:
            website = website.with_respect_robots_txt(self.respect_robots_txt)
    
        if self.accept_invalid_certs is not None:
            website = website.with_danger_accept_invalid_certs(self.accept_invalid_certs)

        if is_scrape:
            website = website.with_return_page_links(True)

        website = website.build()
        return website


class SpiderTools(str, Enum):
    CRAWL = "crawl"
    SCRAPE = "scrape"


async def crawl_url(args: SpiderArgs) -> str:
    website = args.build_website(False)
    website.crawl(headless=True)
    return '\n'.join(website.get_links())


async def scrape_url(args: SpiderArgs) -> str:
    website = args.build_website(True)
    website.scrape(headless=True)
    
    pages = []
    for page in website.get_pages():
        pages.append(dict(links=list(page.links), url=page.url, html=page.content))
    
    return json.dumps(pages)


async def serve() -> None:
    logger = logging.getLogger(__name__)
    server = Server("mcp-spider")

    logger.info("Using mcp-spider")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name=SpiderTools.CRAWL,
                description="Crawls the given url and returns a list of URLs",
                inputSchema=SpiderArgs.model_json_schema(),
            ),
            Tool(
                name=SpiderTools.SCRAPE,
                description="Scrapes the given url and returns a list of URLs along with their contents. The output is in JSON format",
                inputSchema=SpiderArgs.model_json_schema(),
            )
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        match name:
            case SpiderTools.CRAWL:
                crawl_args = SpiderArgs(**arguments)
                result = await crawl_url(crawl_args)
                return [TextContent(type="text", text=f"crawled links:\n{result}")]
            case SpiderTools.SCRAPE:
                scrape_args = SpiderArgs(**arguments)
                result = await scrape_url(scrape_args)
                return [TextContent(type="text", text=f"scrape result:\n{result}")]

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
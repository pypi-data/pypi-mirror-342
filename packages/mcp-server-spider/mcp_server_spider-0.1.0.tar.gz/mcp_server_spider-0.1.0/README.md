# mcp-server-spider: A spider MCP server
## Overview
A Model Context Protocol server for Spider crawler interaction and automation. This server provides tools to crawl and scrape web pages.

Please note that mcp-server-spider is currently in early develpoment. There might be bugs and features added in the future.

### Tools

1. `crawl`
    - Crawls the given url and returns the list of URLs that were found
    - Input:
        - `url`: The url to crawl
        - `headers`: Additional headers passed along with crawl requests
        - `user_agent`: User agent to use for the crawl requests
        - `depth`: The depth of link traversal
        - `blacklist`: A list of regural expression to blacklist URLs from the crawling process
        - `whitelist`: A list of regular expression to whitelist URLS from the crawling process
        - `respect_robots_txt`: Whether to respect `robots.txt` file
        - `accept_invalid_certs`: Whether to accept invalid certifcates or not
    - Returns: List of URLs found
2. `scrape`
    - Scrapes the given url and returns a list of JSON objects that contain the url, links and content of each page discovered
    - Input: Same as `crawl`
    - Returns: A list of JSON objects (as a string) that contain the url, links and content of each page discovered

## Installation

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *mcp-server-spider*.

### Using PIP

Alternatively you can install `mcp-server-spider` via pip:

```
pip install mcp-server-spider
```

After installation, you can run it as a script using:

```
python -m mcp_server_spider
```

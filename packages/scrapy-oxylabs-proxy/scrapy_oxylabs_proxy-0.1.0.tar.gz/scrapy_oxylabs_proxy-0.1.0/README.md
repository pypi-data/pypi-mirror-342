# Scrapy Oxylabs Proxy Middleware

Use Oxylabs Web Scraper API in proxy mode with your Scrapy spiders.

## Installation

```bash
pip install scrapy-oxylabs-proxy
```

## Usage

In `settings.py` of your Scrapy project:

```python
DOWNLOADER_MIDDLEWARES = {
    'scrapy_oxylabs_proxy.middleware.OxylabsWebScraperApiProxyMiddleware': 350,
}

OXYLABS_WS_USER = 'your_oxylabs_username'
OXYLABS_WS_PASSWORD = 'your_oxylabs_password'
OXYLABS_WS_ENDPOINT = 'https://realtime.oxylabs.io:60000'
```

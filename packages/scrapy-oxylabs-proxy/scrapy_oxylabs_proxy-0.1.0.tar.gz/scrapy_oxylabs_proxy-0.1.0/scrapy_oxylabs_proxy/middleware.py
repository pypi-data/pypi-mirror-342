import base64

class OxylabsWebScraperApiProxyMiddleware:
    def __init__(self, user, password, endpoint):
        self.user = user
        self.password = password
        self.endpoint = endpoint
        self.proxy_auth = "Basic " + base64.b64encode(
            f"{user}:{password}".encode("utf-8")
        ).decode("utf-8")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user=crawler.settings.get("OXYLABS_WS_USER"),
            password=crawler.settings.get("OXYLABS_WS_PASSWORD"),
            endpoint=crawler.settings.get("OXYLABS_WS_ENDPOINT", "https://realtime.oxylabs.io:60000"),
        )

    def process_request(self, request, spider):
        request.meta['proxy'] = self.endpoint
        request.headers['Proxy-Authorization'] = self.proxy_auth

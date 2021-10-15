import pytest
from parsel import Selector
from scrapy import Request, Spider
from scrapy.http import HtmlResponse, TextResponse

from tests import make_handler
from tests.mockserver import StaticMockServer, MockProxyServer, \
    MockAioHttpServer


class BaseProxyRequestsMixin:
    @pytest.mark.asyncio
    async def test_request(self):
        settings = {
            "PLAYWRIGHT_BROWSER_TYPE": self.browser_type,
        }
        with MockAioHttpServer() as server:
            with MockProxyServer() as proxy:
                settings["PLAYWRIGHT_CONTEXTS"] = {
                    "1": {
                        "proxy": {
                            "server": proxy.url
                        }
                    }
                }
                async with make_handler(settings) as handler:
                    meta = {
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_context": "1"
                    }
                    req = Request(server.urljoin("/headers"), meta=meta)
                    resp = await handler._download_request(req, Spider("foo"))
                    # JSON response is wrapped in html here, so need to fall
                    # back to html in aiohttp server
                    sel = Selector(text=resp.text, type='html')
                    headers = sel.css('li::text').extract()
                    assert 'X-Proxy-Header=True' in headers

            assert isinstance(resp, TextResponse)


class TestProxyFirefox(BaseProxyRequestsMixin):
    browser_type = 'firefox'

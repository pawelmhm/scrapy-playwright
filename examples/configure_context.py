from pathlib import Path

from playwright.async_api import BrowserContext
from scrapy import Spider, Request
from scrapy.crawler import CrawlerProcess
from scrapy_playwright.page import PageCoroutine


async def configure_context(name: str, context: BrowserContext) -> None:
    await context.route("**/*.jpg", lambda route: route.abort())


class ConfigureContextSpider(Spider):
    """
    Abort the download of images
    """

    name = "configure_context"

    def start_requests(self):
        yield Request(
            url="http://books.toscrape.com/",
            meta={
                "playwright": True,
                "playwright_page_coroutines": [
                    PageCoroutine(
                        "screenshot",
                        path=Path(__file__).parent / "configure_context.png",
                        full_page=True,
                    ),
                ],
            },
        )

    def parse(self, response):
        yield {"url": response.url}


if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            "DOWNLOAD_HANDLERS": {
                # "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },
            "PLAYWRIGHT_CONFIGURE_CONTEXT": configure_context,
        }
    )
    process.crawl(ConfigureContextSpider)
    process.start()

import scrapy
import logging

from webspider.items import ImageItem

logger = logging.getLogger(__name__)


class Wallpaper(scrapy.Spider):
    name = 'bizhi88'
    allowed_domains = ['www.bizhi88.com']
    start_urls = ['http://www.bizhi88.com/']

    def parse(self, response, **kwargs):
        for img in response.xpath("//img[@class='lazy']"):
            item = ImageItem(
                title=img.xpath("./@alt").get(""),
                url=img.xpath("./@src").get(""),
            )
            logger.info(item)
            # yield item


if __name__ == '__main__':
    from utils.scrapy import run_spider

    run_spider(locals())

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import attr


@attr.s(auto_attribs=True)
class ImageItem:
    title: str = ""
    url: str = ""

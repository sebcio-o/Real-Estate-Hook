import scrapy
import re

from property_crawler.items import Property


class GumtreeSpider(scrapy.Spider):
    name = "Gumtree"
    BASE_URL = "https://www.gumtree.pl"
    start_urls = [
        "https://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/plock/v1c9008l3200071p1"
    ]

    def parse(self, response):
        cards = response.css(".tileV1")
        for card in cards:
            thumbnail = card.css("source::attr(data-srcset)").get()
            if not thumbnail:
                continue
            price = card.css(".ad-price::text").get()
            title = card.css(".tile-title-text::text").get()
            link = card.css("a::attr(href)").get()
            address = card.css(".description span::text").get()

            if link:
                link = self.BASE_URL + link
            if price:
                price = re.sub(r"\D", "", price)

            yield Property(
                site=self.name,
                thumbnail=thumbnail,
                price=price,
                title=title,
                address=address,
                rooms=0,
                link=link,
            )

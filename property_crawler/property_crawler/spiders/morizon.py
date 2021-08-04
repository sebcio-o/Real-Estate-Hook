import scrapy
import re

from property_crawler.items import Property


class MorizonSpider(scrapy.Spider):
    name = "Morizon"
    BASE_URL = "https://www.morizon.pl/"
    start_urls = ["https://www.morizon.pl/do-wynajecia/mieszkania/plock/"]

    def parse(self, response):
        cards = response.css(
            "#contentPage > div.contentBox > div > div > div > section .mz-card__item"
        )
        for card in cards:
            thumbnail = card.css("img::attr(src)").get()
            price = card.css(".single-result__price::text").get()
            title = card.css(".single-result__title::text").get()
            link = card.css("a::attr(href)").get()
            rooms = card.css("li:nth-child(1) b::text").get()

            if price:
                price = int(re.sub(r"\D", "", price))
            if rooms:
                rooms = int(re.sub(r"\D", "", rooms))

            yield Property(
                site=self.name,
                thumbnail=thumbnail,
                price=price,
                title=title,
                address="Płock",
                rooms=rooms,
                link=link,
            )

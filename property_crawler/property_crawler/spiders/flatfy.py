import scrapy
import re

from property_crawler.items import Property


class FlatfySpider(scrapy.Spider):
    name = "Flatfy"
    BASE_URL = "https://flatfy.pl"
    start_urls = ["https://flatfy.pl/search?geo_id=992&section_id=2&sort=insert_time"]

    def parse(self, response):
        cards = response.css(".feed-layout__item-holder")
        for card in cards:
            price = card.css(".realty-preview__price::text").get()
            title = card.css(".realty-preview__title-link::text").get()
            link = card.css("a::attr(href)").get()
            rooms = card.css(".realty-preview__info.rooms::text").get()

            if price:
                price = re.sub(r"\D", "", price)
            if link:
                link = self.BASE_URL + card.css("a::attr(href)").get()
            if rooms:
                rooms = re.sub(r"\D", "", rooms)

            yield Property(
                site=self.name,
                thumbnail=None,
                price=price,
                title=title,
                address="Płock",
                rooms=rooms,
                link=link,
            )

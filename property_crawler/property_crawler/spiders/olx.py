import scrapy
import re

from property_crawler.items import Property


class OlxSpider(scrapy.Spider):
    name = "Olx"
    start_urls = ["https://www.olx.pl/plock/q-na-wynajem-mieszkanie/"]

    def parse(self, response):
        cards = response.css(".offer-wrapper")
        for card in cards:
            thumbnail = card.css("img::attr(src)").get()
            price = card.css(".price strong").get()
            title = card.css("h3 strong::text").get()
            link = card.css("a::attr(href)").get()

            if thumbnail:
                thumbnail = "https://www.olx.pl/" + thumbnail
            if link:
                link = "https://www.olx.pl/" + link
            if price:
                price = re.sub(r"\D", "", price)

            yield Property(
                site=self.name,
                thumbnail=thumbnail,
                price=price,
                title=title,
                address="Płock",
                rooms=0,
                link=link,
            )

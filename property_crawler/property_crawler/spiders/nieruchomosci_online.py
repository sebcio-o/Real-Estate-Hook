import scrapy
import re

from property_crawler.items import Property


class NieruchomosciOnlineSpider(scrapy.Spider):
    name = "Nieruchomosci Online"
    start_urls = ["https://plock.nieruchomosci-online.pl/mieszkania,wynajem/"]

    def parse(self, response):
        cards = response.css("#tilesWrapper > div:nth-child(3) > div") + response.css(
            "#tilesWrapper > div:nth-child(5) > div"
        )
        for card in cards:
            thumbnail = card.css("img::attr(src)").get()
            price = card.css(".title-a.primary-display span:nth-child(1)::text").get()
            title = card.css(".province__wrapper h2::text").get()
            link = card.css("a::attr(href)").get()
            address = card.css(".province__wrapper p::text").get()

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

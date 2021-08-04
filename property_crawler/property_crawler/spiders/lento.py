import scrapy
import re

from property_crawler.items import Property


class LentoSpider(scrapy.Spider):
    name = "Lento"
    start_urls = [
        "https://plock.lento.pl/nieruchomosci/mieszkania/do-wynajecia.html?price_to=3000&has_photos=1"
    ]

    def parse(self, response):
        cards = response.css("div.hash")
        for card in cards:
            thumbnail = card.css("img::attr(data-src)").get()
            price = card.css(".price-list-item::text").get()
            title = card.css(".title-list-item::text").get()
            link = card.css("a::attr(href)").get()
            rooms = card.css(
                "div.desc-list-row.desc-list-row-cover-show > div.param-list-row > div.param-list-item.param-list-atrr-item > span:nth-child(2)::text"
            ).getall()
            address = card.css(
                "div.atr-list-row.nowrap-tooltip.hidden-xs .mark-pointer.licon-pin-f::text"
            ).get()

            if price:
                price = int(re.sub(r"\D", "", price))
            if rooms:
                rooms = int(re.sub(r"\D", "", rooms[1]))

            yield Property(
                site=self.name,
                thumbnail=thumbnail,
                price=price,
                title=title,
                address=address,
                rooms=rooms,
                link=link,
            )

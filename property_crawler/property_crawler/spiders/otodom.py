import scrapy
import re

from property_crawler.items import Property


class OtodomSpider(scrapy.Spider):
    name = "Otodom"
    BASE_URL = "https://www.otodom.pl/"
    start_urls = [
        "https://www.otodom.pl/pl/oferty/wynajem/mieszkanie/plock?limit=72&page=1&by=LATEST&direction=DESC"
    ]

    def parse(self, response):
        cards = response.css("ul.css-14cy79a.e3x1uf06 > li")
        for card in cards:
            thumbnail = card.css("img::attr(src)").get()
            price = card.css(".es62z2j16::text").get()
            title = card.css("h3::text").get()
            address = card.css(".css-17o293g.es62z2j19::text").get()
            rooms = card.css(".es62z2j17::text").get()
            link = card.css("a::attr(href)").get()

            if link:
                link = self.BASE_URL + link
            if price:
                price = re.sub(r"\D", "", price)
            if rooms:
                rooms = rooms.split()[0]

            yield Property(
                site=self.name,
                thumbnail=thumbnail,
                price=price,
                title=title,
                address=address,
                rooms=rooms,
                link=link,
            )

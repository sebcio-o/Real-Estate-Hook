import scrapy
import re

from property_crawler.items import Property


class GieldaPlockaSpider(scrapy.Spider):
    name = "Gielda Plocka"
    BASE_URL = "https://www.gieldaplocka.pl/"
    start_urls = ["https://www.gieldaplocka.pl/plock_mieszkania_2_1_0_3.html"]

    def parse(self, response):
        cards = response.css(".lista")
        for card in cards:
            thumbnail = card.css("img::attr(src)").get()
            price = card.css(".pri").get()
            title = card.css(".wi250::text").get()
            link = card.css("a::attr(href)").get()
            address = card.css("li:nth-child(3).wi150::text").get()

            if thumbnail:
                thumbnail = self.BASE_URL + thumbnail
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

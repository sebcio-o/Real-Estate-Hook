from scrapy.item import Field, Item


class Property(Item):
    thumbnail = Field()
    site = Field()
    price = Field()
    link = Field()
    title = Field()
    rooms = Field()
    address = Field()

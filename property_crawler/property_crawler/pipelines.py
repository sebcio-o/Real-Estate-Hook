import os

import requests

import validators
from sqlalchemy.orm import sessionmaker
from time import sleep

from .models import Property, create_items_table, db_connect


class PropertyCrawlerPipeline:
    def __init__(self):
        engine = db_connect()
        create_items_table(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def _get_prepared_message(self, property):
        return f"""

**Nowa nieruchomość z {property['site']}**
**Cena**: {int(property['price'])}
**Tytuł**: {property['title'].strip()}
**Adres**: {property['address']}
**Pokoje**: {property['rooms']}
{property['thumbnail']} {property['link']}
"""

    def process_item(self, property, spider):

        price = int(property["price"])
        link = property["link"]
        p = Property(**property)

        try:
            self.session.add(p)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            return property

        if not validators.url(link):
            return property
        if not price >= 900 and not price <= 2000:
            return property

        sleep(5)
        r = requests.post(
            os.environ["WEBHOOK_URL"],
            json={"content": self._get_prepared_message(property)},
        )
        if r.status_code != 204:
            print(r.json())
        return property

    def close_spider(self, spider):
        print(spider)
        self.session.close()

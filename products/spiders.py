from decimal import Decimal

import requests
import scrapy
from django.conf import settings


class MileSpider(scrapy.Spider):
    name = "mile.by"
    allowed_domains = ["mile.by"]
    start_urls = ["https://mile.by/catalog/elektroinstrument/"]

    def download_image(self, url: str) -> str:
        file_name = url.split("/")[-1]
        r = requests.get(f"https://mile.by{url}", stream=True)
        if r.status_code == 200:
            with open(settings.MEDIA_ROOT / file_name, "wb") as f:
                for chunk in r:
                    f.write(chunk)
        return file_name

    def parse(self, response, **kwargs):
        for product in response.css(".showcase-sorting-block .anons-wrap"):
            image_link = product.css(".anons-foto img::attr(src)").get()
            image_name = self.download_image(image_link)
            price = product.css(".anons-price-wrap .price span::text").get()
            price = price.strip().split(".")[0] if price is not None else 0
            data = {
                "external_id": int(
                    product.css(".anons-sku::text").get().replace("Арт. ", "")
                ),
                "title": product.css(".anons-name a::text").get().strip(),
                "price": Decimal(price),
                "image": image_name,
            }
            yield data

        next_page = response.css(
            ".pagination-wrap .pagin-arrow:last-child::attr(href)"
        ).get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

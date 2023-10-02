import scrapy
from scrapy.linkextractors import LinkExtractor

from .spider_tools.extractors import Extractors


class ColesScraper(scrapy.Spider):
    name = "coles_scraper"  # identifies the Spider. It must be unique within a project.
    start_urls = [
        "https://www.coles.com.au/browse/meat-seafood?pid=homepage_cat_explorer_meat_seafood",
        "https://www.coles.com.au/browse/fruit-vegetables",
        "https://www.coles.com.au/browse/dairy-eggs-fridge",
        "https://www.coles.com.au/browse/bakery",
        "https://www.coles.com.au/browse/deli",
        "https://www.coles.com.au/browse/pantry",
        "https://www.coles.com.au/browse/drinks",
        "https://www.coles.com.au/browse/frozen"
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.links = list()
        self.link_extractor = LinkExtractor(allow=r"/product",
                                            restrict_css="#coles-targeting-product-tiles")
        self.page_number = 0

    def parse(self, response, **kwargs):
        """
        The parse() method usually parses the response, extracting the scraped data as dicts
        and also finding new URLs to follow and creating new requests (Request) from them.
        """

        extractor = Extractors()

        for link in self.link_extractor.extract_links(response=response):
            yield scrapy.Request(link.url, callback=self.parse_page)

        last_page_link = response.css("#coles-targeting-browse-content-container > nav > ul a::attr(href)").getall()[-1]
        last_page_number = extractor.get_last_page(last_page_link)

        if self.page_number < last_page_number:
            self.page_number += 1
            next_page = f"?page={self.page_number}"
            yield response.follow(next_page, self.parse)

    @staticmethod
    def parse_page(response):

        product_name = response.css('h1::text').get()
        price = response.css(".price__value::text").get()
        unit_price = response.css(".price__calculation_method::text").get()

        data = {
            "product_name": product_name,
            "price": price,
            "unit_price": unit_price
        }

        yield data

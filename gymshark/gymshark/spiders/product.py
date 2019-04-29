import re
import json

import requests
import scrapy

from instagram.instagram.items import InstagramProfileItem

p = r"(?P<script_stat><script type=\"text/javascript\">window\._sharedData = )(?P<config>.+)(?P<script_end>;</script>)"
PAGE_CONFIG_PATTERN = re.compile(p)


class ProductSpider(scrapy.Spider):
    """Gymshark product spider"""

    name = 'gymshark_products'

    allowed_domains = ['uk.gymshark.com']

    base_url = 'https://uk.gymshark.com'

    start_urls = [
        'https://uk.gymshark.com/collections/all-products/womens'
    ]

    def parse_product(self, response):
        """Parse product page"""
        self.log(f'Parse product: {response.url}')

    def parse(self, response):
        """Parse main page with pagination"""
        current_page = int(response.css('span.page.current strong::text').get())
        max_page = int(response.xpath("//span[@class='next']/preceding-sibling::span[@class='page'][1]/a/text()").get())

        for product_item in response.css('div.product-grid div.grid__item'):
            

            for profile in chain(profile['followers'], profile['following']):
                profile_link = f"{self.base_url}/{profile['username']}/"
                yield response.follow(url=profile_link, cookies=dict(self.requests_cookies), callback=self.parse)

            yield profile

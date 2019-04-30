import re
import json

import scrapy

from gymshark.items import GymsharkItem

p = r"(?P<conf_start>var gtmPushData =\s)(?P<config>{[^;]+ee-productView[^;]+})(?P<conf_end>;)"
PAGE_CONFIG_PATTERN = re.compile(p)


class ProductSpider(scrapy.Spider):
    """Gymshark product spider"""

    name = 'gymshark_products'

    allowed_domains = ['uk.gymshark.com']

    schema = 'https'

    base_url = 'https://uk.gymshark.com'

    all_products_pagination = 'collections/all-products/womens'

    start_urls = [
        f'{base_url}/{all_products_pagination}'
    ]

    def parse_product(self, response):
        """Parse product page"""
        self.log(f'Parse product: {response.url}')

        match = PAGE_CONFIG_PATTERN.search(response.text)

        if match:
            try:
                config = match.groupdict()['config']
                products_meta = json.loads(config.replace("'", '"'))

                current_product = products_meta['ecommerce']['detail']['products'][0]
            except (json.JSONDecodeError, KeyError, IndexError, AttributeError) as e:
                self.log(f'Config parsing error: {str(e)}')
            else:
                product = GymsharkItem(
                    id=current_product['id'],
                    url=response.url,
                    name=current_product['name'],
                    price=current_product['price'],
                    category=current_product['category'],
                )

                images = response.css('ul.support__images.desktop--images img::attr(src)').extract() or []
                images.extend(response.css('div#featureimage img::attr(src)').extract())

                product['images'] = [f'{self.schema}:{url}' for url in images]

                yield product

    def parse(self, response):
        """Parse main page with pagination"""
        current_page = int(response.css('span.page.current strong::text').get())
        next_page = current_page + 1
        max_page = int(response.xpath("//span[@class='next']/preceding-sibling::span[@class='page'][1]/a/text()").get())

        for product_url in response.css('div.product-grid div.grid__item div.prod-image-wrap a::attr(href)').extract():
            yield scrapy.Request(url=f'{self.base_url}{product_url}', callback=self.parse_product)

        if next_page <= max_page:
            next_page_url = f'{self.base_url}/{self.all_products_pagination}?page={next_page}'
            yield response.follow(url=next_page_url, callback=self.parse)

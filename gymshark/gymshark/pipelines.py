# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import re

from requests.utils import urlparse
from scrapy import Request
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline

from .utils import slugify
from .settings import ASSETS_DIR, SPLIT_PRODUCTS_BY_CATEGORY

IMAGE_SIZE_PATTERN = re.compile(r'(?P<width>\d+)(?P<x>x)(?P<height>\d+)')


class GymsharkPipeline(object):

    def process_item(self, item, spider):
        """Save item to JSON"""
        base_dir = ASSETS_DIR

        if SPLIT_PRODUCTS_BY_CATEGORY:
            try:
                category_dir = os.path.join(ASSETS_DIR, slugify(item['category']))
            except (re.error, Exception):
                category_dir = ''

            if category_dir and not os.path.exists(category_dir):
                os.mkdir(category_dir)

            base_dir = os.path.join(base_dir, category_dir)

        product_dir = os.path.join(base_dir, item['id'])

        if not os.path.exists(product_dir):
            os.mkdir(product_dir)

        with open(os.path.join(product_dir, 'info.json'), 'wb') as f:
            exporter = JsonItemExporter(file=f, encoding='utf-8', indent=4)
            exporter.export_item(item)

        return item


class ProductImagesPipeline(ImagesPipeline):
    """Download & save item photos to specified directory"""

    def get_media_requests(self, item, info):
        """Async images downloading"""
        base_dir = ''

        if SPLIT_PRODUCTS_BY_CATEGORY:
            try:
                category_dir = slugify(item['category'])
            except (re.error, Exception):
                category_dir = ''

            base_dir = category_dir

        base_dir = os.path.join(base_dir, item['id'])

        for image in item['images']:
            yield Request(image, meta={'base_dir': base_dir, 'url': image})

    def file_path(self, request, response=None, info=None):
        image_guid = os.path.split(urlparse(request.meta['url']).path)[1]

        match = IMAGE_SIZE_PATTERN.search(request.meta['url'])

        if match:
            subdir = match.group()
        else:
            subdir = ''

        return os.path.join(request.meta['base_dir'], subdir, image_guid)

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
from contextlib import closing
import asyncio

import aiohttp
import aiofiles
from requests.utils import urlparse

from .settings import ASSETS_DIR


class GymsharkPipeline(object):

    async def download_file(self, session, url, download_dir):
        """Async file downloading
        :param session: aiohttp.ClientSession()
        :param download_dir: target directory
        """
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()

                filename = os.path.split(urlparse(url).path)[1]  # extract filename from URL

                async with aiofiles.open(os.path.join(download_dir, filename), 'wb') as f:
                    await f.write(content)

    async def download_files(self, urls, download_dir):
        """Async downloading via Aiohttp
        :param urls: files to download
        :param download_dir: target directory
        """
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False, limit=1)) as session:
            tasks = []
            for url in urls:
                tasks.append(self.download_file(session=session, url=url, download_dir=download_dir))
            await asyncio.gather(*tasks)

    def process_item(self, item, spider):
        """Pipeline item processing
        :param item: result of 'spider.parse' method
        :param spider: current spider
        :return: processed item
        """
        product_dir = os.path.join(ASSETS_DIR, item['id'])

        if not os.path.exists(product_dir):
            os.mkdir(product_dir)

        with open(os.path.join(product_dir, 'info.json'), 'w') as f:
            f.write(json.dumps(item, indent=4))

        with closing(asyncio.new_event_loop()) as loop:
            loop.run_until_complete(self.download_files(item['photos'], download_dir=product_dir))

        return item

import os
import re

import scrapy
from scrapy.crawler import CrawlerProcess

from DataProcess import DataProcess

class ChapterSpider(scrapy.Spider):
    name = "chapter"

    def __init__(self, novel="", chapters=[], **kwargs):
        self.start_urls = [f'https://daonovel.com/novel/{novel}/{chapter}/' for chapter in sorted(chapters)]
        super().__init__(**kwargs) 

    def parse(self, response):
        folder = os.path.join( __file__, "..", "Content" )

        title = response.css("ol.breadcrumb li.active::text").get().rstrip().lstrip()
        filename = os.path.join(folder, f'{DataProcess.make_file_friendly_name(title)}.html')
        
        container = response.css("div.cha-words p").getall() if response.css("div.cha-words p").getall() else  response.css("div.text-left p").getall()
        content = []
        for p in container:
            raw = str(p)
            content += [DataProcess.fix_bracket(s) for s in re.findall("^<p>(.+)</p>$", raw)]
        content = str('\n\n').join(content)

        with open(filename, "w+", encoding='utf-8') as f:
            f.write(response.headers)
            # f.write(DataProcess.encode_text(content))
            f.write(content)

class NovelSpider(scrapy.Spider):
    name = "novel"

    def __init__(self, novels=[], **kwargs):
        self.start_urls = [f'https://daonovel.com/novel/{novel}' for novel in sorted(novels)]
        super().__init__(**kwargs) 

    def parse(self, response):
        folder = os.path.join( __file__, "..", "Content" )

        title = response.css("ol.breadcrumb li.active::text").get().rstrip().lstrip()
        filename = os.path.join(folder, f'{DataProcess.make_file_friendly_name(title)}.html')
        
        container = response.css("div.cha-words p").getall() if response.css("div.cha-words p").getall() else  response.css("div.text-left p").getall()
        content = []
        for p in container:
            raw = str(p)
            content += [DataProcess.fix_bracket(s) for s in re.findall("^<p>(.+)</p>$", raw)]
        content = str('\n\n').join(content)

        with open(filename, "w+", encoding='utf-8') as f:
            # f.write(DataProcess.encode_text(content))
            f.write(response.headers)
            f.write(content)

    
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(ChapterSpider, novel="mmorpg-rebirth-of-the-legendary-guardian", chapters=["chapter-8"])
    process.start()
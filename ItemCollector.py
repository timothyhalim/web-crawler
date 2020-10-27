import re

from scrapy.crawler import CrawlerProcess
from scrapy import signals

import Controller
import Spider
from DataProcess import DataProcess

class ChapterCollector():
    def __init__(self, book, chapters=[]):
        self.process = CrawlerProcess()
        self.items = []
        self.book = book
        self.chapters = chapters

    def collect(self, item, response, spider):
        #Cleanup
        content = []
        for line in item['content']:
            content += [DataProcess.fix_bracket(s.strip()) for s in re.findall("^<p>(.+)</p>$", line)]
        item['content'] = str("\n").join(content)

        self.items.append(item)

    def create_crawler(self):
        # we need Crawler instance to access signals
        crawler = self.process.create_crawler(Spider.ChapterSpider)
        crawler.signals.connect(self.collect, signal=signals.item_scraped)
        x = self.process.crawl(crawler, book=self.book, chapters=self.chapters)
        return x
    
    def run(self):
        self.create_crawler()
        self.process.start()


class BookCollector():
    def __init__(self, books):
        self.process = CrawlerProcess()
        self.items = []
        self.books = books

    def collect(self, item, response, spider):
        item['authors'] = [author.strip() for author in item['authors']]
        item['genres'] = [genre.strip for genre in item['genres']]

        summary = []
        for line in item['summary']:
            if not any(word in line.lower() for word in ("wuxiaworld", "disclaimer")) :
                summary += [DataProcess.fix_bracket(s) for s in re.findall("^<p>(.+)</p>$", line)]
        item['summary'] = str("\n").join(summary)
        self.items.append(item)

    def create_crawler(self):
        # we need Crawler instance to access signals
        crawler = self.process.create_crawler(Spider.BookSpider)
        crawler.signals.connect(self.collect, signal=signals.item_scraped)
        x = self.process.crawl(crawler, books=self.books)
        return x
    
    def run(self):
        self.create_crawler()
        self.process.start()

# collector = ChapterCollector("mmorpg-rebirth-of-the-legendary-guardian", ["chapter-8", "chapter-9", "chapter-10"])
# collector.run()
# print(collector.items)

collector = BookCollector("reincarnation-of-the-strongest-sword-god-webnovel")
collector.run()
print(collector.items)

# try:
#     init()
#     author = create_author("Timothy")
#     book = create_book("New Book", authors=["new", author, "new", "NEW"], genres=["Action", "Romance"], summary="Summary", status="Complete")
#     chapter = create_chapter

# except Exception as e: 
#     print(traceback.format_exc())


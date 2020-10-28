import re

from scrapy import signals

from . import Spider
from .DataProcess import DataProcess

class Collector():
    def __init__(self, process, books=[]):
        self.process = process
        if isinstance(books, str):
            books = [books]
        self.books = books
        self.books_data = []

    def create_crawler(self, spider, function, **kwargs):
        # we need Crawler instance to access signals
        crawler = self.process.create_crawler(spider)
        crawler.signals.connect(function, signal=signals.item_scraped)
        x = self.process.crawl(crawler, **kwargs)
        return x

    def process_book_data(self, item, response, spider):
        item['authors'] = [author.strip() for author in item['authors']]
        item['genres'] = [genre.strip() for genre in item['genres']]

        summary = []
        for line in item['summary']:
            if not any(word in line.lower() for word in ("wuxiaworld", "disclaimer")) :
                summary += [DataProcess.fix_bracket(s) for s in re.findall("^<p>(.+)</p>$", line)]
        item['summary'] = str("\n").join(summary)

        item['chapters'] = [chapter.replace(item['fullurl'], '').replace('/', '') for chapter in item['chapters']]
        self.books_data.append(item)

    def process_chapter_data(self, item, response, spider):
        #Cleanup
        content = []
        for line in item['content']:
            content += [DataProcess.fix_bracket(s.strip()) for s in re.findall("^<p>(.+)</p>$", line)]
        item['content'] = str("\n").join(content)
        
        for book in self.books_data:
            if book['url'] == item['book_url']:
                book['chapters'][book['chapters'].index(item['url'])] = item
    
    def crawl_books(self):
        return self.create_crawler(Spider.BookSpider, self.process_book_data, books=self.books)
    
    def crawl_chapters(self, book, chapters):
        return self.create_crawler(Spider.ChapterSpider, self.process_chapter_data, book=book, chapters=chapters)


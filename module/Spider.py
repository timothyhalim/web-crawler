import re

import scrapy

from . import Controller
from .DataProcess import DataProcess

class ReaderSpider(scrapy.Spider):
    name = "book"

    def __init__(self, books=[], **kwargs):
        if isinstance(books,str):
            books = [books]
        Controller.init()
        self.start_urls = [f'https://daonovel.com/novel/{book}/' for book in sorted(books)]
        super().__init__(**kwargs) 

    def parse(self, response):
        # Compile Data
        book = {
            'fullurl' : response.url,
            'url' : response.url.split("/")[-2],
            'title' : response.css("div.post-title h1::text").extract()[-1].strip(),
            'authors' : response.css('div.author-content a::text').getall(),
            'genres' : response.css('div.genres-content a::text').getall(),
            'status' : response.css('div.post-status div.post-content_item:nth-child(2) div.summary-content::text').get().strip(),
            'release' : response.css('div.post-status div.post-content_item:nth-child(1) div.summary-content::text').get().strip()\
                    if response.css('div.post-status div.post-content_item:nth-child(1) div.summary-content::text').get().strip() \
                    else str(response.css('div.post-status div.post-content_item:nth-child(1) div.summary-content a::text').get().strip()),
            'summary' : response.css('div.summary__content p').getall(),
            'chapters' : []
        }
        # Cleanup Data
        book['authors'] = [author.strip() for author in book['authors']]
        book['genres'] = [genre.strip() for genre in book['genres']]

        summary = []
        for line in book['summary']:
            if not any(word in line.lower() for word in ("wuxiaworld", "disclaimer")) :
                summary += [DataProcess.fix_bracket(s) for s in re.findall("^<p>(.+)</p>$", line)]
        book['summary'] = str("\n").join(summary)

        #Submit to db
        book = Controller.create_book(
                        book['title'], 
                        book['fullurl'], 
                        book['url'], 
                        authors=book['authors'], 
                        genres=book['genres'], 
                        summary=DataProcess.encode_text(book['summary']), 
                        status=book['status'], 
                        release=book['release']
                    )

        # Iterate and fetch chapter
        fetched_url = [chapter.fullurl for chapter in book.chapters()]
        chapter_urls = [url for url in response.css('ul.version-chap li a::attr(href)').extract() if not url in fetched_url] #filter already scrapped chapter
        if chapter_urls:
            for chapter_url in chapter_urls: # Loop For Async Request for faster scrap
                yield scrapy.Request(
                    url=chapter_url,
                    callback=self.parse_chapter,
                    meta={'book': book}
                )

    def parse_chapter(self, response):
        book = response.meta['book']
        
        container = response.css("div.cha-words p").getall() if response.css("div.cha-words p").getall() else response.css("div.text-left p").getall()
        content = []
        for line in [str(p) for p in container]:
            content += [DataProcess.fix_bracket(s.strip()) for s in re.findall("^<p>(.+)</p>$", line)]
        content = str("\n").join(content)

        chapter = {
            'title' : response.css("ol.breadcrumb li.active::text").get().strip(),
            'content' : content,
            'fullurl' : response.url,
            'url' : response.url.split("/")[-2],
        }
        chapter = Controller.create_chapter(
                            book, 
                            chapter['title'], 
                            chapter['fullurl'], 
                            chapter['url'], 
                            content=DataProcess.encode_text(chapter['content']), 
                            is_published=True
                        )

        yield book
        
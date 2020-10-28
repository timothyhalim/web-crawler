### Spider
import scrapy

class BookSpider(scrapy.Spider):
    name = "book"

    def __init__(self, books=[], **kwargs):
        if isinstance(books,str):
            books = [books]
        self.start_urls = [f'https://daonovel.com/novel/{book}/' for book in sorted(books)]
        super().__init__(**kwargs) 

    def parse(self, response):
        # self.remove_content(response.css("div.post-title h1 span"))
        fullurl = response.url
        url = fullurl.split("/")[-2]
        title = response.css("div.post-title h1::text").extract()
        title = title[len(title)-1].strip()
        authors = response.css('div.author-content a::text').getall()
        genres = response.css('div.genres-content a::text').getall()
        release = response.css('div.post-status div.post-content_item:nth-child(1) div.summary-content::text').get().strip()
        status = response.css('div.post-status div.post-content_item:nth-child(2) div.summary-content::text').get().strip()
        summary = response.css('div.summary__content p').getall()

        chapters = response.css('ul.version-chap li a::attr(href)').extract()
        chapters.reverse()

        return {
            'fullurl' : fullurl,
            'url' : url,
            'title' : title,
            'authors' : authors,
            'genres' : genres,
            'status' : status,
            'release' : release,
            'summary' : summary,
            'chapters' : chapters
        }

class ChapterSpider(scrapy.Spider):
    name = "chapter"

    def __init__(self, book="", chapters=[], **kwargs):
        if isinstance(chapters,str):
            chapters = [chapters]
        self.book = book
        self.start_urls = [f'https://daonovel.com/novel/{book}/{chapter}/' for chapter in chapters]
        super().__init__(**kwargs) 

    def parse(self, response):
        title = response.css("ol.breadcrumb li.active::text").get().strip()
        
        container = response.css("div.cha-words p").getall() if response.css("div.cha-words p").getall() else  response.css("div.text-left p").getall()
        content = []
        for p in container:
            content.append(str(p))
        
        return {
            'title' : title,
            'content' : content,
            'book_url': self.book,
            'url' : response.url.split("/")[-2]
        }
        
# from scrapy.crawler import CrawlerProcess
# process = CrawlerProcess()
# process.crawl(BookSpider, book="a-stay-at-home-dads-restaurant-in-an-alternate-world")
# process.start()

# Collector
from scrapy import signals
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor

class Collector():
    def __init__(self, books=[]):
        if isinstance(books, str):
            books = [books]
        self.books = books
        self.books_data = []

    def create_crawler(self, process, spider, callback, **kwargs):
        # we need Crawler instance to access signals
        crawler = process.create_crawler(spider)
        crawler.signals.connect(callback, signal=signals.item_scraped)
        x = process.crawl(crawler, **kwargs)
        return x

    def process_book_data(self, item, response, spider):
        item['authors'] = [author.strip() for author in item['authors']]
        item['genres'] = [genre.strip() for genre in item['genres']]

        summary = [line for line in item['summary'] if not any(word in line.lower() for word in ("wuxiaworld", "disclaimer"))]
        item['summary'] = str("\n").join(summary)

        item['chapters'] = [chapter.replace(item['fullurl'], '').replace('/', '') for chapter in item['chapters']]
        self.books_data.append(item)

    def process_chapter_data(self, item, response, spider):
        item['content'] = str("\n").join(item['content'])
        
        for book in self.books_data:
            if book['url'] == item['book_url']:
                book['chapters'][book['chapters'].index(item['url'])] = item
    
    def crawl_books(self):
        return self.create_crawler(BookSpider, self.process_book_data, books=self.books)
    
    def crawl_chapters(self, book, chapters):
        return self.create_crawler(ChapterSpider, self.process_chapter_data, book=book, chapters=chapters)

    def run(self, spider, callback, **kwargs):
        def f(q):
            try:
                runner = crawler.CrawlerRunner()
                deferred = self.create_crawler(runner, spider, callback, **kwargs)
                deferred.addBoth(lambda _: reactor.stop())
                reactor.run()
                q.put(None)
            except Exception as e:
                q.put(e)

        q = Queue()
        p = Process(target=f, args=(q,))
        p.start()
        result = q.get()
        p.join()

        if result is not None:
            raise result

# Execute
# from scrapy.crawler import CrawlerProcess
# process = CrawlerProcess()
# collector = Collector(process, books="a-stay-at-home-dads-restaurant-in-an-alternate-world")
# collector.crawl_books()
# collector.crawl_chapters("a-stay-at-home-dads-restaurant-in-an-alternate-world", ['chapter-1', 'chapter-2', 'chapter-3', 'chapter-4', 'chapter-5'])
# process.start()

# for book in (collector.books_data):
#     for k,v in book.items():
#         print(k,v)
# the wrapper to make it run more times

def run(collector, spider, callback, **kwargs):
    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            deferred = collector.create_crawler(runner, spider, callback, **kwargs)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result
collector = Collector(books="a-stay-at-home-dads-restaurant-in-an-alternate-world")
run(collector, BookSpider, collector.process_book_data, books=collector.books)
print ( collector.books_data )

# book = create_book(item['title'], authors=item['authors'], genres=item['genres'], summary=item['summary'], status=item['status'])
# for item in chapter_data.items:
#     create_chapter(book, item['title'], content=item['content'], is_published=True)
# try:
#     init()
#     author = create_author("Timothy")
#     
#     chapter = create_chapter

# except Exception as e: 
#     print(traceback.format_exc())

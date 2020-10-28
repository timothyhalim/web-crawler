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
        print(response.url)
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
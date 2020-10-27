import scrapy

class ChapterSpider(scrapy.Spider):
    name = "chapter"

    def __init__(self, book="", chapters=[], **kwargs):
        if isinstance(chapters,str):
            chapters = [chapters]
        self.start_urls = [f'https://daonovel.com/novel/{book}/{chapter}/' for chapter in sorted(chapters)]
        super().__init__(**kwargs) 

    def parse(self, response):
        title = response.css("ol.breadcrumb li.active::text").get().strip()
        
        container = response.css("div.cha-words p").getall() if response.css("div.cha-words p").getall() else  response.css("div.text-left p").getall()
        content = []
        for p in container:
            content.append(str(p))
        
        return {
            'title' : title,
            'content' : content
        }
        
class BookSpider(scrapy.Spider):
    name = "book"

    def __init__(self, books=[], **kwargs):
        if isinstance(books,str):
            books = [books]
        print(books)
        self.start_urls = [f'https://daonovel.com/novel/{book}/' for book in sorted(books)]
        super().__init__(**kwargs) 

    def remove_content(self, to_remove):
        if to_remove:
            to_remove = to_remove[0].root
            to_remove.getparent().remove(to_remove)

    def parse(self, response):
        # self.remove_content(response.css("div.post-title h1 span"))

        title = response.css("div.post-title h1::text").extract()
        title = title[len(title)-1].strip()
        authors = response.css('div.author-content a::text').getall()
        genres = response.css('div.genres-content a::text').getall()
        summary = response.css('div.summary__content p').getall()

        chapters = response.css('ul.version-chap li a::attr(href)').extract()
        chapters.reverse()

        return {
            'title' : title,
            'authors' : authors,
            'genres' : genres,
            'summary' : summary,
            # 'chapters' : chapters
        }

# from scrapy.crawler import CrawlerProcess
# process = CrawlerProcess()
# process.crawl(BookSpider, book="a-stay-at-home-dads-restaurant-in-an-alternate-world")
# process.start()
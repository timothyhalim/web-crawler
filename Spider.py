import scrapy

class ChapterSpider(scrapy.Spider):
    name = "chapter"

    def __init__(self, book="", chapters=[], **kwargs):
        self.start_urls = [f'https://daonovel.com/novel/{book}/{chapter}/' for chapter in sorted(chapters)]
        super().__init__(**kwargs) 

    def parse(self, response):
        title = response.css("ol.breadcrumb li.active::text").get().rstrip().lstrip()
        
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
        self.start_urls = [f'https://daonovel.com/novel/{book}/' for book in sorted(books)]
        super().__init__(**kwargs) 

    def parse(self, response):
        title = response.css("ol.breadcrumb li.active::text").get().rstrip().lstrip()
        
        container = response.css("div.cha-words p").getall() if response.css("div.cha-words p").getall() else  response.css("div.text-left p").getall()
        content = []
        for p in container:
            content.append(str(p))
        
        return {
            'title' : title,
            'content' : content
        }
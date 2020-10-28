from scrapy import Spider
from scrapy.http import Request, FormRequest
from scrapy.utils.response import open_in_browser


class LarmSpider(Spider):
    name = 'larm'
    allowed_domains = ['larmtjanst.se']
    start_urls = ['https://www.larmtjanst.se/Efterlysta-objekt/Personbil/?s=True']

    def parse(self, response):
        yield FormRequest('https://www.larmtjanst.se/StolenItemsHelper/SearchAjax?category=Personbil',
                          formdata={'category': 'Personbil'},
                          callback=self.parse_form)

    def parse_form(self, response):
        open_in_browser(response)
        table = response.xpath('//*[contains(@class, "searchResultTable")]')[1]
        trs = table.xpath('.//tr')
        for tr in trs:
            reg_num = tr.xpath('.//td/a/text()').extract_first()

            yield {
                'Register Number': reg_num
            }

from scrapy.crawler import CrawlerProcess
process = CrawlerProcess()
process.crawl(LarmSpider)
process.start()
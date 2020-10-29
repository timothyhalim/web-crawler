from scrapy.crawler import CrawlerProcess
from module.Spider import ReaderSpider

from module import Controller
from module.Model import db, Author, Genre, Status, Book, Chapter, BookAuthor, BookGenre


# Controller.init()
# Controller.create_book(
#     title='A Stay-at-home Dad’s Restaurant In An Alternate World',
#     fullurl='https://daonovel.com/novel/a-stay-at-home-dads-restaurant-in-an-alternate-world/',
#     url='a-stay-at-home-dads-restaurant-in-an-alternate-world',
#     summary= '''<p>In Chaos City on the Norland Continent, there is a strange restaurant.</p>
# <p>Here, elves are stuffing kebabs, paying no mind to their manners; giant dragons are sitting around a hot pot, strainers in their hands; demons are eating nice-looking dango…</p>
# <p>They have to follow weird, strict rules if they wishto eat here; yet, that doesn’t stop them from lining up in front of this restaurant.</p>
# <p>They talk about how divine the food here is and how talented the chef is. Nobody ever dares of dining and dashing.</p>
# <p>“Pay, now!” says a cute little girl in her childish voice. A five-meter tall dragon shivers when it meets her eyes.</p>''',
#     release='Updating',
#     status='OnGoing',
#     authors=['Whispering Jianghu'],
#     genres=['Comedy', 'Fantasy', 'Slice of Life'],
# )


process = CrawlerProcess()
process.crawl(ReaderSpider, books="a-stay-at-home-dads-restaurant-in-an-alternate-world")
process.start()
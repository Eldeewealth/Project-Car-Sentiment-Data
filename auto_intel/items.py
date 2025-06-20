# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
   
import scrapy

class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    publication_date = scrapy.Field()
    author = scrapy.Field()
    source = scrapy.Field()

class CarReviewItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    publication_date = scrapy.Field()
    author = scrapy.Field()
    source = scrapy.Field()
    verdict = scrapy.Field()
    rating = scrapy.Field()

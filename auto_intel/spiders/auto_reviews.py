import scrapy
from auto_intel.items import CarReviewItem  # ✅ updated import
from datetime import datetime
from w3lib.html import remove_tags

class AutoReviewsSpider(scrapy.Spider):
    name = "auto_reviews"
    allowed_domains = ["autoexpress.co.uk"]
    start_urls = ["https://www.autoexpress.co.uk/car-reviews"]
    page_count = 1  # start from page 1
    max_pages = 6  # limit to 10 pages

    def parse(self, response):
        article_links = response.css("a.polaris__link.polaris__article-card--link::attr(href)").getall()
        for link in article_links:
            yield response.follow(response.urljoin(link), callback=self.parse_article)

        # Pagination logic – follow "Load More" if under max_pages
        if self.page_count < self.max_pages:
            next_page = response.css("a.polaris__link.polaris__load-more--link::attr(href)").get()
            if next_page:
                self.page_count += 1
                yield response.follow(response.urljoin(next_page), callback=self.parse)

    def parse_article(self, response):
        item = CarReviewItem()  # ✅ use CarReviewItem not ArticleItem

        item['title'] = response.css("h1.polaris__heading::text").get()

        date_text = response.css("span.polaris__date::text").get()
        if date_text:
            try:
                pub_date = datetime.strptime(date_text.strip().title(), "%d %b %Y").date()
            except ValueError:
                pub_date = None
        else:
            pub_date = None
        item['publication_date'] = pub_date

        item['source'] = "Auto Express"

        author = response.css("span.polaris__post-meta--author-name a::text").get()
        item['author'] = author.strip() if author else None

        verdict_node = response.xpath(
    "//div[contains(@class, 'polaris__simple-grid--main')"
    " and (h2[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'verdict')]"
    " or h2[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'our opinion')])]"
    "//p[1]").get()

        item['verdict'] = remove_tags(verdict_node).strip() if verdict_node else None

        rating_text = response.css("p.polaris__rating--text::text").get()
        if rating_text:
            try:
                item['rating'] = str(float(rating_text.strip()))
            except ValueError:
                item['rating'] = None
        else:
            item['rating'] = None

        item['link'] = response.url
        yield item

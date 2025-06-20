import scrapy
from auto_intel.items import ArticleItem
from datetime import datetime

class AutoNewsSpider(scrapy.Spider):
    name = "auto_news"
    allowed_domains = ["autoexpress.co.uk"]
   
    def start_requests(self):
        base_urls = [
        "https://www.autoexpress.co.uk/car-news",
        "https://www.autoexpress.co.uk/consumer-issues"]

        for base in base_urls:
            for page in range(1, 4):  # Pages 1 to 10
                url = base if page == 1 else f"{base}?page={page}"
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        articles = response.css("a.polaris__link.polaris__article-card--link")

        for article in articles:
            item = ArticleItem()

            title = article.css("::text").get()
            link = article.attrib.get("href")

            date_text = article.css("span.polaris__date::text").get()
            if date_text:
                try:
                    pub_date = datetime.strptime(date_text.strip().title(), "%d %b %Y").strftime("%d %b %Y")
                except ValueError:
                    pub_date = None
            else:
                pub_date = None

            item['title'] = title.strip() if title else None
            item['link'] = response.urljoin(link)
            item['publication_date'] = pub_date
            item['source'] = "Auto Express"

            # ✅ Call parse_article properly
            yield response.follow(item['link'], callback=self.parse_article, meta={'item': item})

    # ✅ This method is now inside the class
    def parse_article(self, response):
        item = response.meta['item']

    # ✅ Author extraction using correct span class
        authors = response.css("span.polaris__post-meta--author-name a::text").getall()
        author = ", ".join([a.strip() for a in authors]) if authors else None
        item['author'] = author

    # ✅ Get publication date from visible text on article page
        if not item.get('publication_date'):
            date_text = response.css("span.polaris__date::text").get()
            if date_text:
                try:
                    # Handles e.g., '8 Jun 2025' or '08 Jun 2025'
                    pub_date = datetime.strptime(date_text.strip().title(), "%d %b %Y").strftime("%d %b %Y")
                    item['publication_date'] = pub_date
                except ValueError:
                    item['publication_date'] = None

        yield item


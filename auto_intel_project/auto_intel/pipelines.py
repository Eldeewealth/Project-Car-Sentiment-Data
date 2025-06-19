import psycopg2
from scrapy.exceptions import DropItem
from auto_intel.models import ArticleModel, CarReviewModel
from scrapy import Spider
from auto_intel.items import ArticleItem, CarReviewItem  # Add this import, adjust path if needed


class UnifiedPostgresPipeline:
    def open_spider(self, spider):
        self.connection = psycopg2.connect(
            host='localhost',
            dbname='auto_intel_db',
            user='postgres',
            password='Eldeewealth20'
        )
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        try:
            if isinstance(item, CarReviewItem):
                validated = CarReviewModel(**item)
                print("✅ Inserting into car_reviews:", validated.title)
                self.cursor.execute("""
                    INSERT INTO car_reviews (title, link, publication_date, source, author, verdict, rating)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (link) DO NOTHING
                """, (
                    validated.title,
                    str(validated.link),
                    validated.publication_date,
                    validated.source,
                    validated.author,
                    validated.verdict,
                    validated.rating
                ))

            else:  # default to ArticleItem
                validated = ArticleModel(**item)
                print("✅ Inserting into articles:", validated.title)
                self.cursor.execute("""
                    INSERT INTO articles (title, link, publication_date, source, author)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (link) DO NOTHING
                """, (
                    validated.title,
                    str(validated.link),
                    validated.publication_date,
                    validated.source,
                    validated.author
                ))

            self.connection.commit()

        except Exception as e:
            spider.logger.warning(f"❌ Error saving item: {e}")
            raise DropItem(f"Pipeline error: {e}")

        return item
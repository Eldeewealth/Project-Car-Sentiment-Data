from pydantic import BaseModel, HttpUrl, field_validator, validator
from typing import Optional
from datetime import datetime

class ArticleModel(BaseModel):
    title: str
    link: HttpUrl
    publication_date: Optional[str]
    author: Optional[str]
    source: str

    @validator("publication_date", pre=True)
    def validate_date(cls, value):
        if value:
            try:
                # Convert '8 Jun 2025' to ISO: '2025-06-08'
                return datetime.strptime(value.strip(), "%d %b %Y").date().isoformat()
            except ValueError:
                raise ValueError("Invalid date format, expected 'd Mmm YYYY'")
        return value

class CarReviewModel(BaseModel):
    title: str
    link: HttpUrl
    publication_date: Optional[datetime]
    source: str
    author: Optional[str]
    verdict: Optional[str]
    rating: Optional[str]

    @field_validator('title', 'source')
    @classmethod
    def validate_non_empty(cls, value):
        if not value or not value.strip():
            raise ValueError("Field must not be empty or whitespace")
        return value

    @field_validator('rating')
    @classmethod
    def validate_rating(cls, value):
        # Accept values like "4.5 out of 5", "9/10", or just "5"
        if value and not any(char.isdigit() for char in value):
            raise ValueError("Rating must contain numeric value")
        return value
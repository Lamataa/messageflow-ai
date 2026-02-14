from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models import MessageStatus, SentimentType

class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)

    class Config:
        json_schema_extra = {
            "example": {
                "content": "Hello, how are you?"
            }
        }

class MessageResponse(BaseModel):
    id: int
    content: str
    status: MessageStatus
    sentiment: Optional[SentimentType] = None
    sentiment_score: Optional[float] = None
    is_spam: int
    created_at: datetime
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class MessageStats(BaseModel):
    total_messages: int
    pending_messages: int
    completed_messages: int
    failed_messages: int
    spam_detected: int
    positive_sentiment: int
    negative_sentiment: int
    neutral_sentiment: int

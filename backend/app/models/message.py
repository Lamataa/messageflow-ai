from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class MessageStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSED = "processed"
    COMPLETED = "completed"
    FAILED = "failed"

class SentimentType(str, enum.Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class Message(Base):

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    status = Column(
        Enum(MessageStatus), 
        default=MessageStatus.PENDING, 
        nullable=False
    )
    sentiment = Column(Enum(SentimentType), nullable=True)
    sentiment_score = Column(Float, nullable=True)
    is_spam = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
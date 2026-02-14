from workers.celery_app import celery_app
from workers.ai_processor import ai_processor
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.models import Message, MessageStatus, SentimentType
from app.models.database import SessionLocal
from datetime import datetime


@celery_app.task(name='message_processing_queue')
def process_message(message_id: int, content: str):
    print(f"Processando mensagem {message_id}...")
    
    db = SessionLocal()
    
    try:
        message = db.query(Message).filter(Message.id == message_id).first()
        
        if not message:
            print(f"Mensagem {message_id} não encontrada!")
            return
        
        message.status = MessageStatus.PROCESSED
        db.commit()
        
        sentiment_type, sentiment_score = ai_processor.analyze_sentiment(content)
        print(f"Sentimento: {sentiment_type} ({sentiment_score:.2f})")
        
        is_spam = ai_processor.detect_spam(content)
        print(f"Spam: {'SIM' if is_spam else 'NÃO'}")
        
        message.sentiment = SentimentType[sentiment_type.upper()]
        message.sentiment_score = sentiment_score
        message.is_spam = is_spam
        message.processed_at = datetime.utcnow()
        message.status = MessageStatus.COMPLETED
        
        db.commit()
        
        print(f"Mensagem {message_id} processada!")
        
        return {
            "message_id": message_id,
            "sentiment": sentiment_type,
            "sentiment_score": sentiment_score,
            "is_spam": is_spam
        }
        
    except Exception as e:
        print(f"Erro: {e}")
        
        message.status = MessageStatus.FAILED
        db.commit()
        
        raise
        
    finally:
        db.close()
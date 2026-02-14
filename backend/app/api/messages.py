from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from app.models import get_db, Message, MessageStatus
from app.schemas import MessageCreate, MessageResponse

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/", response_model=MessageResponse, status_code=201)
async def create_message(
    message_data: MessageCreate, 
    db: Session = Depends(get_db)
):
    new_message = Message(
        content=message_data.content,
        status=MessageStatus.PENDING
    )
    
    db.add(new_message) 
    db.commit()
    db.refresh(new_message)
    
    try:
        from workers.tasks import process_message
        process_message.apply_async(
            args=[new_message.id, new_message.content],
            queue='message_processing_queue'
        )
        print(f"Mensagem {new_message.id} enviada pro Celery!")
    except Exception as e:
        print(f"Erro ao enviar pro Celery: {e}")
    
    return new_message


@router.get("/", response_model=List[MessageResponse])
async def list_messages(db: Session = Depends(get_db)):
    messages = db.query(Message).all()
    return messages


@router.get("/{message_id}", response_model=MessageResponse)
async def get_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return message
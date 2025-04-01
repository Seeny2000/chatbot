from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Chat
from schemas import ChatCreate
from database import get_db
from typing import List

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/send")
def send_message(chat_data: ChatCreate, db: Session = Depends(get_db)):

    existing_chat = db.query(Chat).filter(Chat.user_id == chat_data.user_id).first()

    if not chat_data.user_id:
        raise HTTPException(status_code=400, detail="Please enter user_id")

    # Check if username is provided
    if not chat_data.username:
        raise HTTPException(status_code=400, detail="Please enter username")
    
    if not chat_data.password:
        raise HTTPException(status_code=400, detail="please enter password")

    try:
        chat = Chat(
            user_id=chat_data.user_id,
            message=chat_data.message, 
            response=chat_data.response,
            username=chat_data.username if chat_data.username else "Unknown",
            )
        db.add(chat)
        db.commit()
        db.refresh(chat)
        return {"message": "Message stored successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

@router.get("/history/{user_id}", response_model=List[ChatCreate])
def get_chat_history(user_id: int, db: Session = Depends(get_db)):
    # Validate if user_id is provided
    if not user_id:
        raise HTTPException(status_code=400, detail="Please provide a valid user_id")

    chats = db.query(Chat).filter(Chat.user_id == user_id).all()
    # for chat in chats:
    #     print(chat.username)

    if not chats:
        raise HTTPException(status_code=404, detail="No chat history found")
    
    for chat in chats:
        if chat.response is None:
            chat.response = "No response available"
    
    return chats
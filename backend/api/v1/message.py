from typing import *

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from db import get_db
from model import User
from schema import MessageCreate
from service import UserService, ThreadService, MessageService

router = APIRouter()

@router.post("/threads/{thread_id}/messages")
async def create_message(
    thread_id: int,
    payload: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(UserService.get_current_user),
):
    try:
        existed_thread = ThreadService.getThreadById(thread_id, current_user, db)
        if not existed_thread:
            raise HTTPException(status_code=404, detail="Thread not found.")

        human_message = MessageService.createMessage(payload, thread_id, db)

        # Stream the response
        return StreamingResponse(
            MessageService.responseMessage(human_message, db),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
            },
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
from typing import *

from fastapi import APIRouter, Depends, HTTPException
from fastapi import UploadFile, File as FastAPIFile
from sqlalchemy.orm import Session

from db import get_db
from model import User
from service import UserService, ThreadService, FileService


router = APIRouter()


@router.get("/threads")
def get_threads(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(UserService.login_required)
):
    threads = ThreadService.getThreads(current_user, db, limit=limit, offset=offset)
    return threads


@router.post("/threads")
async def create_thread(
    files: List[UploadFile] = FastAPIFile(...),
    db: Session = Depends(get_db), current_user: User = Depends(UserService.login_required)
):
    if len(files) == 0 or len(files) > 10:
        raise HTTPException(status_code=400, detail="Number of files must be between 1 and 10.")
    
    try:
        new_thread = ThreadService.createThread(current_user, db)           # Create a new thread
        
        success_files, failed_files = [], []                                # Save files
        for file in files:
            try:
                file_content = await file.read()
                size = len(file_content)
                file.file.seek(0)                                           # Reset file pointer after reading
                
                db_file = await FileService.createFile(new_thread.id, file, db)
                success_files.append({
                    "id": db_file.id,
                    "name": db_file.name,
                    "path": db_file.path,
                    "size": size,
                    "content_type": file.content_type
                })
            
            except Exception as e:
                failed_files.append({"filename": file.filename, "error": str(e)})

        if len(success_files) == 0:
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to upload any files.")

        db.commit()
        return {
            "thread": {"id": new_thread.id, "created_at": new_thread.created_at, "updated_at": new_thread.updated_at},
            "success_files": success_files,
            "failed_files": failed_files,
            "total_files": len(files),
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/threads/{thread_id}/messages")
async def get_messages(
    thread_id: int,
    limit: int = 20, offset: int = 0,
    db: Session = Depends(get_db), current_user: User = Depends(UserService.login_required)
):
    """Get messages in a thread"""
    try:
        thread = ThreadService.getThreadById(thread_id, current_user, db)
        if not thread or thread.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Thread not found")
        
        messages = ThreadService.getMessages(thread, db, limit, offset)
        return messages

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
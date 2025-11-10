from fastapi import HTTPException
from sqlalchemy.orm import Session

from model import File, User, Thread, Message


class ThreadService(object):
    @staticmethod
    def getThreadById(thread_id: int, user: User, db: Session) -> Thread | None:
        existed_thread = db.query(Thread).filter(
            Thread.id == thread_id, 
            Thread.user_id == user.id
        ).first()
        
        if existed_thread.user_id != user.id:
            raise HTTPException(status_code=403, detail="You do not have permission to access this thread.")
        
        return existed_thread
    
    
    @staticmethod
    def createThread(user: User, db: Session) -> Thread:
        new_thread = Thread(user_id=user.id)
        db.add(new_thread)
        db.flush()
        return new_thread


    @staticmethod
    def getThreads(user: User, db: Session, limit: int = 10, offset: int = 0):
        threads = db.query(Thread).filter(
            Thread.user_id == user.id
        ).limit(limit).offset(offset).all()

        return threads


    @staticmethod
    def getMessages(thread: Thread, db: Session, limit: int = 10, offset: int = 0) -> list[File]:
        messages = db.query(Message).filter(
            Message.thread_id == thread.id
        ).limit(limit).offset(offset).all()
        
        return messages
    

    @staticmethod
    def getFiles(thread: Thread, db: Session, limit: int = 10, offset: int = 0) -> list[File]:
        files = db.query(File).filter(
            File.thread_id == thread.id
        ).limit(limit).offset(offset).all()

        return files
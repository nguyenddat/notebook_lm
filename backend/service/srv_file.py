import os
import uuid

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi import UploadFile, File as FastAPIFile

from config import config
from model.file import File

class FileService(object):
    @staticmethod
    def getLastIndex(db: Session) -> int:
        return db.query(File).count()

    
    @staticmethod
    async def createFile(
        thread_id: int,
        file: UploadFile,
        db: Session,
    ):
        try:
            """Lưu file vào filesystem"""
            thread_dir = os.path.join(config.artifact_dir, str(thread_id))
            os.makedirs(thread_dir, exist_ok=True)

            file_extension = os.path.splitext(file.filename)[1] if file.filename else ""
            unique_filename = f"{file.filename}-{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(thread_dir, unique_filename)
            
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)

            """Lưu file vào database"""
            db_file = File(
                name=file.filename,
                path=file_path,
                thread_id=thread_id
            )
            db.add(db_file)
            db.flush()
            return db_file
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

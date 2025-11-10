from sqlalchemy.orm import Session

from model import Thread
from model import Message
from schema import MessageCreate
from utils import generate_stream, RAG
from utils.utils_enum import Sender

class MessageService:
    @staticmethod
    def createMessage(payload: MessageCreate, thread_id: int, db: Session):
        content = payload.content
        message = Message(content=content, sender=Sender.HUMAN, thread_id=thread_id)
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    

    @staticmethod
    def responseMessage(human_message: Message, db: Session):
        thread_id = human_message.thread_id
        existed_thread = db.query(Thread).filter(Thread.id == thread_id).first()
        rag = RAG(existed_thread).load_data(db)

        def generator():
            final_resp = ""
            citations = []

            for chunk in rag.invoke(human_message.content):
                if not isinstance(chunk, dict):
                    chunk = dict(chunk)

                final_resp = chunk["response"]
                citations = chunk["citations"]
                yield final_resp
                    
            bot_message = Message(content=final_resp, sender=Sender.AI, thread_id=thread_id)
            db.add(bot_message)
            db.commit()
            db.refresh(bot_message)

            yield {"response": final_resp, "citations": citations}

        return generate_stream(generator())

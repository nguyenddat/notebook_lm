from sqlalchemy import Column, String, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship

from model.base import BareBaseModel
from utils.utils_enum import Sender

class Message(BareBaseModel):
    content = Column(String, nullable=False)
    sender = Column(Enum(Sender, name="sender"), nullable=False)

    thread_id = Column(Integer, ForeignKey("thread.id"), nullable=False)

    thread = relationship("Thread", back_populates="message")
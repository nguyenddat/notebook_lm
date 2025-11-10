from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from model.base import BareBaseModel

class File(BareBaseModel):
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    
    thread_id = Column(Integer, ForeignKey("thread.id"), nullable=False)
    
    thread = relationship("Thread", back_populates="file")
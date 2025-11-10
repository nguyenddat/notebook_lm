from sqlalchemy import *
from sqlalchemy.orm import relationship

from model.base import BareBaseModel

class Thread(BareBaseModel):
    title = Column(String)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="thread")
    message = relationship("Message", back_populates="thread")
    file = relationship("File", back_populates="thread")
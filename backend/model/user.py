from sqlalchemy import *
from sqlalchemy.orm import relationship

from model.base import BareBaseModel

class User(BareBaseModel):
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    role = Column(String, nullable=False)

    thread = relationship("Thread", back_populates="user")

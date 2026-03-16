from database import Base
from sqlalchemy import Column , Integer , String , Boolean

class post(Base):
    __tablename__ = "social_mediapost"

    id = Column(Integer,primary_key = True , nullable=False)
    title = Column(String ,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default='True',nullable=False)
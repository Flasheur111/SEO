from sqlalchemy import Column, Integer, String
from app.database import Base

class Article(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    title = Column(String(120))
    content = Column(String())
    image = Column(String(120))

    def __init__(self, title, content, image):
        self.title = title
        self.content = content
        self.image = image

    def __repr__(self):
        return 'yoerorqeg'

    def to_dict(self):
        return {'title': self.title,
                'content': self.content,
                'image': self.image}

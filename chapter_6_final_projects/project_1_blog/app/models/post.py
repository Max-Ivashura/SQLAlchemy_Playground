from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from chapter_6_final_projects.project_1_blog.app.database import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default=datetime)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))

    users = relationship('User', back_populates='posts')
    categories = relationship('Category', back_populates='posts')

    def __repr__(self):
        return (f"<Post(id='{self.id}', title='{self.title}', content='{self.content}',"
                f" created_at={self.created_at},"
                f" user_id={self.user_id},"
                f" category_id={self.category_id})>")

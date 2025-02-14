from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from chapter_6_final_projects.project_1_blog.app.database import Base


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    created_at = Column(DateTime, default=datetime)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))

    def __repr__(self):
        return (f"<Comment(id={self.id}, text='{self.text}',"
                f" created_at={self.created_at},"
                f" user_id={self.user_id})>")

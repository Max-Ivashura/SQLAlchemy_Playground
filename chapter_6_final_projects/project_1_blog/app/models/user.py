from sqlalchemy import Column, Integer, String

from chapter_6_final_projects.project_1_blog.app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True)
    email = Column(String(20), unique=True)

    def __repr__(self):
        return f"<User(id='{self.id}', username='{self.username}', email='{self.email}')>"

from sqlalchemy import Column, Integer, String

from chapter_6_final_projects.project_1_blog.app.database import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return f"<Category(id='%s', name='%s')>"

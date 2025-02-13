from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

# Промежуточная таблица для связи "многие-ко-многим"
student_course = Table(
    'student_course', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

# Модель Student
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)  # Добавляем unique=True

    courses = relationship('Course', secondary=student_course, back_populates='students')

    def __repr__(self):
        return f'<Student(id={self.id}, name="{self.name}")>'

# Модель Course
class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)  # Добавляем unique=True

    students = relationship('Student', secondary=student_course, back_populates='courses')

    def __repr__(self):
        return f'<Course(id={self.id}, name="{self.name}")>'

# Создаем движок и генерируем таблицы
engine = create_engine('sqlite:///students.db', echo=True)
Base.metadata.create_all(engine)

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

# Добавляем тестовые данные
student_1 = Student(name='Max')
student_2 = Student(name='Mary')
student_3 = Student(name='John')

course_1 = Course(name='Technology')
course_2 = Course(name='Science')
course_3 = Course(name='Math')

student_1.courses = [course_1, course_2]
student_2.courses = [course_2, course_3]
student_3.courses = [course_1, course_3]

session.add_all([student_1, student_2, student_3])
session.commit()

# Запросы с использованием отношений
print("Студенты и их курсы:")
for student in session.query(Student).all():
    print(f"{student.name}:")
    if student.courses:
        for course in student.courses:
            print(f"  - {course.name}")
    else:
        print("  - Нет курсов")

print("\nКурсы и их студенты:")
for course in session.query(Course).all():
    print(f"{course.name}:")
    if course.students:
        for student in course.students:
            print(f"  - {student.name}")
    else:
        print("  - Нет студентов")
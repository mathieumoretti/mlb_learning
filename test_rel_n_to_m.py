from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
db_uri = 'sqlite:///db.sqlite_test'
engine = create_engine(db_uri)
# use session_factory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()


def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()


association_table = Table(
    'association', Base.metadata,
    Column('course_id', Integer, ForeignKey('course.id')),
    Column('student_id', Integer, ForeignKey('student.id'))
)


class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    students = relationship("Student", secondary=association_table)

    def __init__(self, title, description, students):
        self.title = title
        self.description = description
        self.students = students

class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name



def populate_database():
    session = session_factory()

    bruno = Student("Bruno Krebs")
    john = Student("John Doe")
    serena = Student("Serena Williams")
    jennifer = Student("Jennifer Garner")

    tenis = Course("Tenis Introduction", "Learn the basic rules of tenis", [bruno, john])
    chess = Course("Advanced Chess", "Learn advanced strategies", [serena])
    python = Course("Python Development", "Learn the basic concepts of Python", [serena, jennifer, john])

    session.add(tenis)
    session.add(chess)
    session.add(python)

    session.commit()
    session.close()


def query_courses():
    session = session_factory()
    course_query = session.query(Course)
    session.close()
    return course_query.all()


if __name__ == "__main__":
    courses = query_courses()
    if len(courses) == 0:
        populate_database()

        courses = query_courses()
    for course in courses:
        print(f'"{course.title}" has the following students: ', end="")

        for student in course.students:
            print(f'{student.name}; ', end="")

        print('')
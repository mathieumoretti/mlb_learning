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

#Player
class ProjectManager(Base):
    __tablename__ = 'project_manager'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    projects = relationship("Project", back_populates="project_manager")

    def __init__(self, name):
        self.name = name
#Gamelog
class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    #player_id
    project_manager_id = Column(Integer, ForeignKey('project_manager.id'))
    project_manager = relationship("ProjectManager", back_populates="projects")

    def __init__(self, title, description, project_manager):
        self.title = title
        self.description = description
        self.project_manager = project_manager


def populate_database():
    session = session_factory()

    bruno = ProjectManager("Bruno Krebs")
    john = ProjectManager("John Doe")

    todo = Project("To-Do List", "Let's help people accomplish their tasks", bruno)
    moneyfy = Project("Moneyfy", "Best app to manage personal finances", john)
    questionmark = Project("QuestionMark", "App that simulates technical exams", bruno)
    blog = Project("NewBlog", "New blog engine that solves all issues", john)

    session.add(todo)
    session.add(moneyfy)
    session.add(questionmark)
    session.add(blog)

    session.commit()
    session.close()


def query_projects():
    session = session_factory()
    projects_query = session.query(Project)
    session.close()
    return projects_query.all()


if __name__ == "__main__":
    projects = query_projects()
    if len(projects) == 0:
        populate_database()

    projects = query_projects()
    for project in projects:
        print(f'"{project.title}" is managed by {project.project_manager.name}')
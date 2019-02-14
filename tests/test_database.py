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


class Mobile(Base):
    __tablename__ = 'mobile'

    id = Column(Integer, primary_key=True)
    model = Column(String)
    number = Column(String)
    owner_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, model, number, owner):
        self.model = model
        self.number = number
        self.owner = owner

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    mobile = relationship("Mobile", uselist=False, backref="owner")

    def __init__(self, name):
        self.name = name


def populate_database():
    session = session_factory()

    bruno = User("Bruno Krebs")
    john = User("John Doe")

    brunos_mobile = Mobile("android", "99991111", bruno)
    johns_mobile = Mobile("iphone", "55554444", john)

    session.add(brunos_mobile)
    session.add(johns_mobile)

    session.commit()
    session.close()


def query_users():
    session = session_factory()
    users_query = session.query(User)
    session.close()
    return users_query.all()


def query_mobiles():
    session = session_factory()
    mobiles_query = session.query(Mobile)
    session.close()
    return mobiles_query.all()


def test_database():
    users = query_users()
    if len(users) == 0:
        populate_database()

    users = query_users()
    for user in users:
        print(f'{user.name} has an {user.mobile.model} with number {user.mobile.number}')

    someVar = 2
    assert 2 == someVar

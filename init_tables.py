from models import Base
from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg2://postgres:qwerty@localhost/sqlalchemy_system")
engine.connect()
Base.metadata.drop_all(engine)
from models import Student
from models import Teacher
from models import Subject
from models import GroupTeacherSubject
Base.metadata.create_all(engine)

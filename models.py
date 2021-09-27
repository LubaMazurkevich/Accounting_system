from sqlalchemy import Integer,Column,ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class GroupTeacherSubject(Base):
    __tablename__ = 'Group_teacher_subject'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer(), ForeignKey("groups.id"))
    subject_id = Column(Integer(), ForeignKey("subjects.id"))
    teacher_id = Column(Integer(), ForeignKey("teachers.id"))


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer(), primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False)
    subjects_groups = relationship("GroupTeacherSubject", backref='teacher')


def create_teacher(session):
    t = Teacher(
        first_name=input("Введите имя преподавателя: "),
        last_name=input("Введите фамилию преподавателя: "),
        email=input("Введите e-mail преподавателя: ")
    )
    session.add(t)
    session.commit()
    print(f"Вы добавили преподавателя {t.first_name} {t.last_name}")
    return t


def show_teachers(session):
    print("Преподаватели: ")
    teachers = session.query(Teacher)
    if teachers.count() == 0:
        print("Преподаватели отсутствуют") 
    for teacher in teachers:
        print(teacher.id, teacher.first_name, teacher.last_name, teacher.email)



class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)
    groups_teachers = relationship("GroupTeacherSubject", backref='subject')


def create_subject(session):
    sb = Subject(name=input("Введите название предмета: "))
    session.add(sb)
    session.commit()
    print(f"Вы добавили предмет {sb.name}")
    return sb


def show_subjects(session):
    print("Предметы: ")
    subjects = session.query(Subject)
    if subjects.count() == 0:
        print("Предметы отсутствуют")
    for subject in subjects:
        print(subject.id, subject.name)


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)
    students = relationship("Student")
    subjects_teachers = relationship("GroupTeacherSubject", backref='group')


def create_group(session):
    g = Group(name=input("Введите название группы: "))
    session.add(g)
    session.commit()
    print(f"Вы добавили группу {g.name}")
    return g


def show_groups(session):
    print("Группы:")
    groups = session.query(Group)
    if groups.count() == 0:
        print("Группы отсутствуют")
    for group in groups:
        print(group.id, group.name)


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer(), primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))


def create_student(session):
    s = Student(
        first_name=input("Введите имя студента: "),
        last_name=input("Введите фамилию студента: "),
        email=input("Введите e-mail студента: ")
    )
    session.add(s)
    session.commit()
    print(f"Вы добавили студента {s.first_name} {s.last_name}")
    return s


def show_students(session):
    print("Студенты: ")
    students = session.query(Student)
    if students.count() == 0:
        print("Студенты отсутствуют")
    for student in students:
        print(student.id, student.first_name, student.last_name, student.email)

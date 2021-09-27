from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData
from models import *


def create_main_menu(session):
    temp = receive_from_consol("Введите,что хотите сделать:\n1)Просмотр записей\n2)Добавление записей\
                            \n3)Удаление записей\n4)Редактирование записей\n")
    if temp == 1:
        show_menu(session)
    if temp == 2:
        add_menu(session)
    if temp == 3:
        delete_menu(session)
    if temp == 4:
        redact_menu(session)


def show_menu(session):
    temp = receive_from_consol("Просмотр:\n1)студентов\n2)преподавателей\n3)групп\n4)предметов\n0)назад\n")
    if temp == 1:
        show_links_student(session)
    if temp == 2:
        show_teachers(session)
        show_links_teacher(session)
    if temp == 3:
        show_groups(session)
        show_links_group(session)
    if temp == 4:
        show_subjects(session)
        show_links_subject(session)
    if temp == 0:
        create_main_menu(session)


def add_menu(session):
    temp = receive_from_consol("Добавить:\n1)Cтудента\n2)Преподавателя\n3)Группу\n4)Предмет\n"
                               "0)Назад\n")
    if temp == 1:
        add_student(session)
    if temp == 2:
        create_teacher(session)
    if temp == 3:
        create_group(session)
    if temp == 4:
        create_subject(session)
    if temp == 0:
        create_main_menu(session)


def delete_menu(session):
    temp = receive_from_consol("Выберите что хотите сделать:\n1)удалить студента\n"
                                "2)удалить преподавателя\n3)удалить предмет\n"
                                "4)удалить группу\n0)назад\n")
    if temp == 1:
        show_students(session)
        s_id = receive_from_consol("Введите id студента которого нужно удалить или 0 чтобы вернуться назад: ")
        if s_id == 0:
            delete_menu(session)
        else:
            student = session.query(Student).get(s_id)
            session.delete(student)
            session.commit()
            print("Вы удалили студента!")
    elif temp == 2:
        delete_teacher(session)
    elif temp == 3:
        delete_subject(session)
    elif temp == 4:
        delete_group(session)
    elif temp == 0:
        create_main_menu(session)


def redact_menu(session):
    temp = receive_from_consol("Редактировать:\n1)студентов\n2)преподавателей\n"
                               "3)группы\n4)предметы\n0)назад\n")
    if temp == 1:
        redact_student(session)
    if temp == 2:
        redact_teacher(session)
    if temp == 3:
        show_groups(session)
        temp = receive_from_consol("Редактировать:\n1)Название группы\n"
                                   "2)Добавить предмет и преподавателя группе\n"
                                   "3)Удалить предмет и преподавателя из группы\n0)Назад\n")
        if temp == 1:
            show_groups(session)
            s_id = receive_from_consol("Введите id группы для редактирования или 0 чтобы вернуться назад: ")
            if s_id == 0:
                redact_menu(session)
            else:
                group = session.query(Group).get(s_id)
                group.name = input("Введите новое название группы: ")
                session.add(group)
                session.commit()
        if temp == 2:
            add_subject_to_group(session)
        if temp == 3:
            show_groups(session)
            s_id = receive_from_consol("Введите id группы связь которой нужно удалить или 0 чтобы вернуться назад: ")
            if s_id ==0:
                redact_menu(session)
            else:
                try:
                    gr_tc_sb = session.query(GroupTeacherSubject).filter(GroupTeacherSubject.group_id == s_id).all()
                    for i in gr_tc_sb:
                        session.delete(i)
                except:
                    pass
            session.commit()
            if temp == 0:
                redact_menu(session)
        if temp == 0:
            redact_menu(session)
    if temp == 4:
        show_subjects(session)
        s_id = receive_from_consol("Введите id предмета для редактирования или 0 чтобы вернуться назад: ")
        if s_id == 0:
            redact_menu(session)
        else:
            subject = session.query(Subject).get(s_id)
            subject.name= input("Введите новое название предмета: ")
            session.add(subject)
            session.commit()
    if temp == 0:
        create_main_menu(session)


def delete_teacher(session):
    show_teachers(session)
    temp = receive_from_consol("Внимание!Если вы удалите преподавателя,который связан с группой и предметом,то предмет и группа останутся без преподавателя.\
     \nВы уверены,что хотите удалить преподавателя?\n1)продолжить\n0)назад\n")
    if temp == 1:
        s_id = receive_from_consol("Введите id преподавателя которого нужно удалить: ")
        teacher = session.query(Teacher).get(s_id)
        try:
            gr_tc_sb = session.query(GroupTeacherSubject).filter(GroupTeacherSubject.teacher_id == s_id).all()
            for i in gr_tc_sb:
                session.delete(i)
        except:
            pass
        session.delete(teacher)
        session.commit()
        print("Вы удалили преподавателя!")
    if temp == 0:
        delete_menu(session)


def delete_group(session):
    show_groups(session)
    temp = receive_from_consol("Внимание!Если вы удалите группу,у которой есть студенты,то студенты останутся без группы!\
    \nВы уверены,что хотите удалить группу?\n1)продолжить\n0)назад\n")
    if temp == 1:
        show_groups(session)
        s_id = receive_from_consol("Введите id группы которую необходимо удалить: ")
        group = session.query(Group).get(s_id)
        try:
            students = session.query(Student).filter(Student.group_id == group.id).all()
            for i in students:
                i.group_id = None
            gr_tc_sb = session.query(GroupTeacherSubject).filter(GroupTeacherSubject.group_id == s_id).all()
            for i in gr_tc_sb:
                session.delete(i)
        except:
            pass
        session.delete(group)
        session.commit()
        print("Вы удалили группу!")
    if temp == 0:
        delete_menu(session)


def delete_subject(session):
    show_subjects(session)
    s_id = receive_from_consol("Введите id предмета который нужно удалить или 0 чтобы вернуться назад: ")
    if s_id == 0:
        delete_menu(session)
    else:
        subject = session.query(Subject).get(s_id)
        try:
            gr_tc_sb = session.query(GroupTeacherSubject).filter(GroupTeacherSubject.subject_id == s_id).all()
            for i in gr_tc_sb:
                session.delete(i)
        except:
            pass
        session.delete(subject)
        session.commit()
        print("Вы удалили предмет!")


def redact_student(session):
    show_students(session)
    s_id = receive_from_consol("1)Введите id студента для редактирования или 0 чтобы вернуться назад: ")
    if s_id == 0:
        redact_menu(session)
    else:
        temp = receive_from_consol("Выберите что хотите отредактировать:\n"
                                   "1)Имя студента\n2)Фамилию студента\n3)e-mail студента\n0)назад\n")
        student = session.query(Student).get(s_id)
        if temp == 1:
            student.first_name = input("Введите новое имя студента: ")
        if temp == 2:
            student.last_name = input("Введите новую фамилию студента: ")
        if temp == 3:
            student.email = input("Введите новый e-mail студента: ")
        if temp == 0:
            redact_menu(session)
        session.add(student)
        session.commit()


def redact_teacher(session):
    show_teachers(session)
    s_id = receive_from_consol("Введите id преподавателя для редактирования или 0 чтобы вернуться назад: ")
    if s_id == 0:
        redact_menu(session)
    else:
        teacher = session.query(Teacher).get(s_id)
        temp = receive_from_consol(
            "Выберите что хотите отредактировать:\n1)Имя преподавателя\n"
            "2)Фамилию преподавателя\n3)e-mail преподавателя\n0)назад")
        if temp == 1:
            teacher.first_name = input("Введите новое имя преподавателя: ")
        elif temp == 2:
            teacher.last_name = input("Введите новую фамилию преподавателя: ")
        elif temp == 3:
            teacher.email = input("Введите новый e-mail преподавателя: ")
        elif temp == 0:
            redact_menu(session)
        session.add(teacher)
        session.commit()


def show_links_subject(session):
    s_id = receive_from_consol("Чтобы узнать подробнее введите номер предмета или введите 0 чтобы вернуться назад:\n")
    if s_id == 0:
        show_menu(session)
    else:
        try:
            subject = session.query(Subject).get(s_id)
            if subject.groups_teachers==[]:
                print("Группа не связана с предметом и преподавателем!")
            for gr_tc_sb in subject.groups_teachers:
                teacher = session.query(Teacher).get(gr_tc_sb.teacher_id)
                group = session.query(Group).get(gr_tc_sb.group_id)
                print(f'Предмет {subject.name} ведет преподаватель {teacher.first_name} '
                      f'{teacher.last_name} в группе {group.name}')
        except:
            print("Данного номера предмета не существует!")


def show_links_group(session):
    g_id = receive_from_consol("Чтобы узнать подробнее введите номер группы или введите 0 чтобы вернуться назад:\n")
    if g_id == 0:
        show_menu(session)
    else:
        try:
            group = session.query(Group).get(g_id)
            if group.subjects_teachers == []:
                print("Группа не связана с предметом и преподавателем!")
            for gr_tc_sb in group.subjects_teachers:
                teacher = session.query(Teacher).get(gr_tc_sb.teacher_id)
                subject = session.query(Subject).get(gr_tc_sb.subject_id)
                print(f'У группы {group.name} ведет преподаватель {teacher.first_name} {teacher.last_name} предмет {subject.name}')
        except:
            print("Данного номера группы не существует!")


def show_links_teacher(session):
    t_id = receive_from_consol("Чтобы узнать подробнее введите номер преподавателя или введите 0 чтобы вернуться назад:\n")
    if t_id == 0:
        show_menu(session)
    else:
        try:
            teacher = session.query(Teacher).get(t_id)
            if teacher.subjects_groups == []:
                print("Преподаватель не связан с группой и предметом!")
            for gr_tc_sb in teacher.subjects_groups:
                subject = session.query(Subject).get(gr_tc_sb.subject_id)
                group = session.query(Group).get(gr_tc_sb.group_id)
                print(
                    f'Преподаватель {teacher.first_name} {teacher.last_name} ведет предмет'
                    f' {subject.name} в группе {group.name}')
        except:
            print("Данного номера преподавателя не существует!")


def show_links_student(session):
    students = session.query(Student)
    if students.count() == 0:
        print("Студенты отсутствуют")
    for st in students:
        if st.group_id != None:
            group=session.query(Group).get(st.group_id)
            print(f"Студент {st.first_name} {st.last_name} {st.email} учится в группе {group.name}")
        else:
            print(f"Студент {st.first_name} {st.last_name} {st.email} не учится")


def add_student(session):
    st = create_student(session)
    temp = receive_from_consol("1)Добавить студента в существующую группу\n2)Добавить студента в новую группу\n"
                               "0)назад\n")
    if temp == 1:
        show_groups(session)
        b = int(input("Введите номер группы в которую нужно добавить студента:"))
        st.group_id = b
    elif temp == 2:
        st.group_id = create_group(session).id
    elif temp == 3:
        create_main_menu(session)


def receive_from_consol(str):
    try:
        return int(input(str))
    except:
        print("Некорректный ввод!")


def add_subject_to_group(session):
    show_groups(session)
    g_id = int(input("Введите номер группы для добавления предмета и преподавателя в группу или 0 чтобы вернуться назад:"))
    if g_id == 0:
        add_menu(session)
    else:
        show_subjects(session)
        c_id = int(input("Введите номер предмета для группы: "))
        show_teachers(session)
        t_id = int(input("Введите номер преподавателя для группы: "))
        gts = GroupTeacherSubject(
            group_id=g_id,
            subject_id=c_id,
            teacher_id=t_id)
        session.add(gts)
        session.commit()


if __name__ == '__main__':
    engine = create_engine("postgresql+psycopg2://postgres:qwerty@localhost/sqlalchemy_system")
    engine.connect()
    metadata = MetaData()
    while True:
        create_main_menu(Session(bind=engine))



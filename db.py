import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import psycopg2

Base = declarative_base()

engine = sq.create_engine('postgresql+psycopg2://владелец_базы_данных:пароль@localhost:5432/имя_базы_данных', client_encoding='utf8')

Session = sessionmaker(bind=engine)

session = Session()
connection = engine.connect()


class User(Base):
    __tablename__ = 'user'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)


class DatingProspect(Base):
    __tablename__ = 'dating_prospect'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    first_name = sq.Column(sq.String)
    second_name = sq.Column(sq.String)
    link = sq.Column(sq.String)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('user.id', ondelete='CASCADE'))


def check_db_user(ids):
    current_user_id = session.query(User).filter_by(vk_id=ids).first()
    return current_user_id


def check_db_prospect(ids):
    dating_user = session.query(DatingProspect).filter_by(
        vk_id=ids).first()
    return dating_user


def register_user(vk_id):
    new_user = User(vk_id=vk_id)
    session.add(new_user)
    session.commit()
    return True


def add_user(vk_id, first_name, second_name, link, id_user):
    new_user = DatingProspect(
        vk_id=vk_id,
        first_name=first_name,
        second_name=second_name,
        link=link,
        id_user=id_user)
    session.add(new_user)
    session.commit()
    return True





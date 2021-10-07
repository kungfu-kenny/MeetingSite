import re
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Table,
                        Text,
                        Column,
                        Integer,
                        String,
                        ForeignKey,
                        PrimaryKeyConstraint)
from sqlalchemy.sql.sqltypes import Boolean


Base = declarative_base()

association_table_user_astrology = Table('user_astrology', Base.metadata,
    Column('id_astrology', ForeignKey('astrology.id')),
    Column('id_user', ForeignKey('user.id')),
    PrimaryKeyConstraint('id_astrology', 'id_user')
)

association_table_user_profession = Table('user_profession', Base.metadata,
    Column('id_profession', ForeignKey('profession.id')),
    Column('id_user', ForeignKey('user.id')),
    PrimaryKeyConstraint('id_profession', 'id_user')
)

association_table_user_gender = Table('user_gender', Base.metadata,
    Column('id_user', ForeignKey('user.id')),
    Column('id_gender', ForeignKey('gender.id')),
    PrimaryKeyConstraint('id_gender', 'id_user')
)

association_table_user_credentials = Table('user_credentials', Base.metadata,
    Column('id_user', ForeignKey('user.id')),
    Column('id_credentials', ForeignKey('credentials.id')),
    PrimaryKeyConstraint('id_credentials', 'id_user')
)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    link = Column(String(100))
    link_image = Column(String(200))
    date_birth = Column(String(20))
    date_death = Column(String(20))
    description = Column(Text)
    is_parsed = Column(Boolean, default=True)
    user_profession = relationship("Profession",
        secondary=association_table_user_profession,
        back_populates="profession_user")
    user_astrology = relationship("Astrology",
        secondary=association_table_user_astrology,
        back_populates="astrology_user")
    user_gender = relationship("Gender",
        secondary=association_table_user_gender,
        back_populates="gender_user")
    user_credentials = relationship('Credentials',
        secondary=association_table_user_credentials,
        back_populates='credentials_user')

class Astrology(Base):
    __tablename__ = 'astrology'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    date_begin = Column(String(10))
    date_end = Column(String(10))
    astrology_user = relationship("User",
        secondary=association_table_user_astrology,
        back_populates="user_astrology")

class Profession(Base):
    __tablename__ = 'profession'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    profession_user = relationship("User",
        secondary=association_table_user_profession,
        back_populates="user_profession")

class Gender(Base):
    __tablename__ = 'gender'
    id = Column(Integer, primary_key=True)
    name = Column(String(10))
    gender_user = relationship("User",
        secondary=association_table_user_gender,
        back_populates="user_gender")

class Credentials(Base):
    __tablename__ = 'credentials'
    id = Column(Integer, primary_key=True)
    email = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    credentials_user = relationship('User',
        secondary=association_table_user_credentials,
        back_populates='user_credentials')

class Selection(Base):
    __tablename__ = 'selection'
    id = Column(Integer, primary_key=True)
    id_selected = Column(Integer)
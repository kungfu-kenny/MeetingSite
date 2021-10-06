from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Table,
                        Text,
                        Column,
                        Integer,
                        String,
                        ForeignKey,
                        PrimaryKeyConstraint)


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

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    link = Column(String(100))
    link_image = Column(String(200))
    date_birth = Column(String(20))
    date_death = Column(String(20))
    description = Column(Text)
    user_profession = relationship("Profession",
        secondary=association_table_user_profession,
        back_populates="profession_user")
    user_astrology = relationship("Astrology",
        secondary=association_table_user_astrology,
        back_populates="astrology_user")

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
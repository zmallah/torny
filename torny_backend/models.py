from sqlalchemy import Column, String, Date, Integer, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base


def get_engine(SQL_URL):
    return create_engine(SQL_URL, echo=True)


Base = declarative_base()


class BoutEventType(Base):
    __tablename__ = 'bout_event_type'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


class CompetitionTypes(Base):
    __tablename__ = 'competition_type'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    usfa_id = Column(String)
    date_of_birth = Column(Date)
    foil_rating = Column(String)
    saber_rating = Column(String)
    epee_rating = Column(String)
    foil_director_rating = Column(String)
    saber_director_rating = Column(String)
    epee_director_rating = Column(String)


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    role = Column(String)


class Tournament(Base):
    __tablename__ = 'tournament'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(Date)
    users = relationship('UserInTournament')
    weapon = Column(String)
    comp_type = ForeignKey('CompetitionTypes')
    location = Column(String)


class UserInTournament(Base):
    __tablename__ = 'user_in_tournament'

    id = Column(Integer, primary_key=True)
    tournament_id = Column(Integer, ForeignKey('tournament.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    role = ForeignKey('Role')
    status = Column(Boolean)
    date_registration = Column(Date)


class Pool(Base):
    __tablename__ = 'pool'

    id = Column(Integer, primary_key=True)
    fencers = relationship('User')
    director = relationship('User')
    tournament = ForeignKey('Tournament')


class Bout(Base):
    __tablename__ = 'bout'

    id = Column(Integer, primary_key=True)
    pool = ForeignKey('Pool')
    fencer_left = Column(Integer, ForeignKey('user.id'))
    fencer_right = Column(Integer, ForeignKey('user.id'))
    fencer_left_score = Column(String)
    fencer_right_score = Column(String)
    completed = Column(Boolean)


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    event_type = Column(String)


class EventLog(Base):
    __tablename__ = 'event_log'

    id = Column(Integer, primary_key=True)
    bout = ForeignKey('Bout')
    event_type = ForeignKey('Event')
    fencer = Column(Integer, ForeignKey('user.id'))
    fencer_left_score = Column(String)
    fencer_right_score = Column(String)

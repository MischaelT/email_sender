from typing import List

from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

db = SQLAlchemy()
BaseModel: DefaultMeta = declarative_base()


class Website(BaseModel):
    __tablename__ = "websites"

    website_id = Column(Integer, unique=True, primary_key=True)
    website_address = Column(Text, unique=True, nullable=False)
    website_name = Column(Text, unique=True, nullable=False)
    creation_date = Column(Text, nullable=False)
    process_is_active = Column(Integer, nullable=False)
    process_start_date = Column(Text, nullable=True)
    stage = Column(Text, nullable=True)
    next_email_date = Column(Text, nullable=False)
    website_type = Column(Text, nullable=False)

    emails = db.relationship('Prospect', backref='websites', lazy=False, uselist=True, cascade="all, delete")

    @classmethod
    def websites_by_isActive_nextEmailDate(cls, session: Session, is_active: int, date: str) -> List["Website"]:
        return session.query(cls).filter_by(process_is_active=is_active, next_email_date=date)

    @classmethod
    def get_website_by_id(cls, session: Session, id: int) -> "Website":
        return session.query(cls).filter_by(website_id=id).all()[0]

    @classmethod
    def get_website_by_email_address(cls, session: Session, address: str) -> "Website":
        return session.query(cls).filter_by(website_address=address).all()[0]

    @classmethod
    def get_website_by_Name_isActive(cls, session: Session, name: str, is_active: int) -> List["Website"]:
        return session.query(cls).filter_by(website_name=name, process_is_active=is_active).all()


class Prospect(BaseModel):

    __tablename__ = "emails"
    email_id = Column(Integer, unique=True, primary_key=True)
    website_id = Column(Integer, db.ForeignKey('websites.website_id'))
    email_address = Column(Text, unique=True, nullable=False)
    last_message_id = Column(Text, unique=True, nullable=False)

    @classmethod
    def get_prospects_by_website_id(cls, session: Session, website_id: int) -> List["Prospect"]:
        return session.query(cls).filter_by(website_id=website_id).all()

    @classmethod
    def get_prospects_by_prospect_id(cls, session: Session, prospect_id: int) -> "Prospect":
        return session.query(cls).filter_by(email_id=prospect_id).all()[0]


class Users(BaseModel):
    __tablename__ = "users"
    user_id = Column(Integer, unique=True, primary_key=True)
    user_name = Column(Text, nullable=False)
    websites_processed = Column(Integer)
    emails_sent = Column(Integer)
    replied = Column(Integer)

    @classmethod
    def get_user_by_name(cls, session: Session, user_name: str) -> "Users":
        return session.query(cls).filter_by(user_name=user_name).all()[0]

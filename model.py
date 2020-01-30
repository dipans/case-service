from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import enum
import datetime
import uuid
from sqlalchemy import Enum

#insert into  "case" (id, case_type, comments, received_date, status_code, case_reference) values(123, 'assessment', 'c', '03-08-2019', 'Active', '1234');
ma = Marshmallow()
db = SQLAlchemy()

#Case
class CaseType(enum.Enum):
    intake=1
    assessment=2
    ongoing=3
    integrated=4

class OwnerRoleType(enum.Enum):
    Owner=1
    Supervisor=2

class Case(db.Model):
    __tablename__ = 'case'
    id = db.Column(db.Integer, primary_key=True)
    case_type = db.Column(db.Enum(CaseType), nullable=False)
    #case_type=db.Column(db.String(250), nullable=False)
    comments=db.Column(db.String(3000))
    received_date=db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)
    status_code=db.Column(db.String(250), nullable=False)
    case_reference=db.Column(db.String, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    #case_owners = db.relationship('CaseUserLink', lazy='select', backref=db.backref('case', lazy='joined' ))
    case_owners = db.relationship('CaseUserLink', backref=db.backref('case'), lazy=False)
    due_date=db.Column(db.DateTime, nullable=True)
    case_participants = db.relationship('CaseParticipantRole', backref=db.backref('case'), lazy=False)

    def __init__(self, case_type, comments, status_code):
        self.case_type = case_type
        self.comments = comments
        self.received_date = datetime.datetime.utcnow()
        self.status_code = status_code
        self.case_reference = str(uuid.uuid4())
        self.due_date = datetime.datetime.utcnow() + datetime.timedelta(days=45)


class CaseUserLink(db.Model):
    __tablename__ = 'case_user_link'
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id', ondelete='CASCADE'), nullable=False)
    #case = db.relationship('Case', backref=db.backref('case_user_link', lazy='dynamic' ))
    user_id = db.Column(db.String, nullable=False)
    owner_role_type = db.Column(db.Enum(OwnerRoleType), nullable=False)

    """ def __init__(self, case_id, user_id):
        self.case_id = case_id
        self.user_id = user_id """

class CaseUserLinkScema(ma.Schema):
    id = fields.Integer(dump_only=True)
    case_id = fields.Integer(required=True)
    user_id = fields.String(required=True)
    owner_role_type = fields.String(required=True)

    #case = ma.Nested(CaseSchema)


class CaseSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    case_type = fields.String(required=True)
    comments = fields.String()
    received_date = fields.DateTime()
    status_code = fields.String()
    creation_date = fields.DateTime()
    case_reference = fields.String()
    due_date = fields.DateTime()
    case_owners = fields.Nested('CaseUserLinkScema', many=True, exclude=('case', ))
    case_participants = fields.Nested('CaseParticipantRoleSchema', many=True, exclude=('case', ))




class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    person_type = db.Column(db.String, nullable=False)
    registration_date=db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)
    status_code=db.Column(db.String, nullable=False)
    date_of_birth=db.Column(db.Date, nullable=True)
    gender=db.Column(db.String, nullable=True)
    first_name=db.Column(db.String, nullable=True)
    middle_name=db.Column(db.String, nullable=True)
    last_name=db.Column(db.String, nullable=True)
    #cases = db.relationship('CaseParticipantRole', backref=db.backref('person'), lazy=False)

    def __init__(self, person_type, status_code, date_of_birth, gender, first_name, middle_name, last_name):
        self.person_type = person_type
        self.registration_date = datetime.datetime.utcnow()
        self.status_code = status_code
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name

class PersonSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    person_type = fields.String(required=True)
    registration_date = fields.DateTime()
    status_code = fields.String()
    date_of_birth = fields.Date()
    gender = fields.String()
    first_name = fields.String()
    middle_name = fields.String()
    last_name = fields.String()

class CaseParticipantRole(db.Model):
    __tablename__ = 'case_participant_role'
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id', ondelete='CASCADE'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id', ondelete='CASCADE'), nullable=False)
    role_type = db.Column(db.String, nullable=False)
    person = db.relationship('Person', backref=db.backref('case_participant_role'), lazy=False)

class CaseParticipantRoleSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    case_id = fields.Integer(required=True)
    person_id = fields.Integer(required=True)
    role_type = fields.String()
    person = fields.Nested('PersonSchema', exclude=('case_participant_role', ))


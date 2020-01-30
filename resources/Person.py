from flask import request
from flask_restful import Resource
from model import db, Case, CaseSchema, CaseUserLink, CaseUserLinkScema, CaseParticipantRoleSchema, Person, PersonSchema
import uuid
from flask import jsonify

persons_schema=PersonSchema(many=True)
person_schema=PersonSchema()

class PersonResource(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        #data, errors = jsonify(json_data)
        #if errors:
        #    return errors, 422
        print(json_data)
        first_name=json_data['first_name']
        last_name=json_data['last_name']
        gender=json_data['gender']
        print(first_name+last_name+gender)

        persons = Person.query.filter(Person.first_name.like(f'%{first_name}%'), Person.last_name.like(f'%{last_name}%'), Person.gender.match(gender.lower())).all()

        #persons = Person.query.filter(Person.first_name.like(f'%{first_name}%')).all()
        persons = persons_schema.dump(persons).data

        return { "status": 'success', 'data': persons}, 200

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data and 'id' not in json_data:
            return {'message': 'No input data provided'}, 400

        # Validate and deserialize input
        data, errors = person_schema.load(json_data)

        db.session.query(Person).filter(Person.id == json_data['id']).update({Person.first_name:json_data['first_name'], Person.middle_name:json_data['middle_name'], Person.last_name:json_data['last_name'], Person.date_of_birth:json_data['date_of_birth'], Person.gender:json_data['gender'], }, synchronize_session = False)
        db.session.commit() 
        result_person = Person.query.filter_by(id=json_data['id']).first() 
        person_json = person_schema.dump(result_person).data

        return { "status": 'success', 'data': "person"}, 200


class PersonSearchResource(Resource): 
    def get(self, first_name=None, last_name=None, gender=None): 
        if first_name==None and last_name==None: 
            return { "status": 'success', 'data': []}, 200 
        elif first_name==None: 
            last_name_like = "%{}%".format(last_name) 
            persons = Person.query.filter(Person.last_name.like(last_name_like), Person.gender.match(gender.lower())).all() 
        elif last_name==None: 
            first_name_like = "%{}%".format(first_name) 
            persons = Person.query.filter(Person.first_name.like(first_name_like), Person.gender.match(gender.lower())).all() 
        else: 
            first_name_like = "%{}%".format(first_name) 
            last_name_like = "%{}%".format(last_name) 
            persons = Person.query.filter(Person.first_name.like(first_name_like), Person.last_name.like(last_name_like), Person.gender.match(gender.lower())).all()
        
        persons = persons_schema.dump(persons).data
        
        return { "status": 'success', 'data': persons}, 200

        
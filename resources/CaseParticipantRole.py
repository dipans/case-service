from flask import request
from flask_restful import Resource
from model import db, Case, CaseSchema, CaseUserLink, CaseUserLinkScema, OwnerRoleType, CaseParticipantRole, CaseParticipantRoleSchema, Person, PersonSchema
import uuid
from flask import jsonify

case_participant_roles_schema = CaseParticipantRoleSchema(many=True)
case_participant_role_schema = CaseParticipantRoleSchema()
case_schema = CaseSchema()
person_schema = PersonSchema()

class CaseParticipantRoleResource(Resource):
    def get(self, case_id):
        participants = CaseParticipantRole.query.filter_by(case_id=case_id).all()
        print(participants)
        participants = case_participant_roles_schema.dump(participants).data
        return {'status': 'success', 'data': participants}, 200
    
    def post(self, case_id):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        #data, errors = case_participant_role_schema.load(json_data)
        #if errors:
        #    return errors, 422
        if 'id' in json_data:
            person_id=json_data['id']
            person = Person.query.filter_by(id=person_id).first()
            role_type=json_data['role_type']
        else:
            
            if 'person_type' in json_data:
                person_type=json_data['person_type']
            else:
                person_type='Person'
            date_of_birth=json_data['date_of_birth']
            status_code='Active'
            gender=json_data['gender']
            first_name=json_data['first_name']
            middle_name=json_data['middle_name']
            last_name=json_data['last_name']
            role_type=json_data['role_type']
            person = Person(person_type, status_code, date_of_birth, gender, first_name, middle_name, last_name)

        case = Case.query.filter_by(id=case_id).first()
        cpr = CaseParticipantRole(role_type=role_type, case_id=case.id, person=person)

        db.session.add(person)
        db.session.add(cpr)
        db.session.commit()
        person_json = person_schema.dump(person).data
        """ participant: {
            "first_name": person.first_name,
            "middle_name": person.middle_name,
            "last_name": person.last_name,
            "date_of_birth": person.date_of_birth.
            "gender": person.gender,
            "status_code": person.status_code,
            "role_type": role_type

        } """
        return { "status": 'success', "data": { "person":person_json, "role_type": role_type}}, 201

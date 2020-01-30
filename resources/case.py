from flask import request
from flask_restful import Resource
from model import db, Case, CaseSchema, CaseUserLink, CaseUserLinkScema, OwnerRoleType
import uuid
from flask import jsonify

cases_schema = CaseSchema(many=True)
case_schema = CaseSchema()
case_link_schema = CaseUserLinkScema(many=True)


class CaseResource(Resource):
    def get(self):
        cases = Case.query.all()
        print(cases[0].status_code)
        cases = cases_schema.dump(cases).data
        print(cases)
        return {'status': 'success', 'data': cases}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = case_schema.load(json_data)
        if errors:
            return errors, 422
        if 'case_reference' in data:
            case = Case.query.filter_by(case_reference=data['case_reference']).first()
            if case:
                return {'message': 'Case already exists'}, 400

        case_type=json_data['case_type']
        comments=json_data['comments']
        status_code=json_data['status_code']
        case = Case(case_type, comments, status_code)

        caseUserLink1 = CaseUserLink(user_id='user123', owner_role_type=OwnerRoleType.Owner, case=case)
        caseUserLink2 = CaseUserLink(user_id='super123', owner_role_type=OwnerRoleType.Supervisor, case=case)
        db.session.add(case)
        db.session.add(caseUserLink1)
        db.session.add(caseUserLink2)
        db.session.commit()


        #result = cases_schema.dump(case).data

        return { "status": 'success', 'data': case_schema.dump(case)}, 201
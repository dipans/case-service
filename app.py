from flask import Blueprint
from flask_restful import Api
from resources.case import CaseResource
from resources.CaseParticipantRole import CaseParticipantRoleResource
from resources.Person import PersonResource, PersonSearchResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

#Endpoints
api.add_resource(CaseResource, '/case')
api.add_resource(CaseParticipantRoleResource, '/case/<string:case_id>/participants')
api.add_resource(PersonResource, '/person')
api.add_resource(PersonSearchResource, '/person/first_name/<string:first_name>/last_name/<string:last_name>/gender/<string:gender>',
        '/person/last_name/<string:last_name>/gender/<string:gender>',
        '/person/first_name/<string:first_name>/gender/<string:gender>')

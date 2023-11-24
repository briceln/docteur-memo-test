import json
import jwt
from datetime import datetime, timedelta, timezone
import os
from werkzeug.exceptions import HTTPException
from flask import Flask, jsonify, request
from flask_api import status
from dotenv import load_dotenv
from marshmallow.exceptions import ValidationError
import requests
from waitress import serve
from paste.translogger import TransLogger
import sentry_sdk
import logging

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

from middlewares.can_access_beta_features import can_access_beta_features
from schema.credentialsSchema import CredentialsSchema
from models.userFactory import UserFactory
from models.patient import Patient

def create_app(config = {}):
    load_dotenv()
    
    sentry_sdk.init(
        dsn="https://4b9d373fb41544353c8a687c642f24c0@o1116557.ingest.sentry.io/4506272493862912",
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        enable_tracing=True
    )

    app = Flask(__name__)
    app.config.from_object(config)

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        response = e.get_response()
        response.data = json.dumps({
            "data": None,
            "error": e.name,
            "message": e.description,
        })
        response.content_type = "application/json"
        return response

    @app.errorhandler(ValidationError)
    def register_validation_error(error):
        rv = dict({'message':  error.messages, "error": "Bad Request", "data": None})
        return rv, status.HTTP_400_BAD_REQUEST

    @app.errorhandler(json.JSONDecodeError)
    def json_decode_error(error):
        rv = dict({'message': 'Received invalid json data', "error": "Bad Request", "data": None})
        return rv, status.HTTP_400_BAD_REQUEST

    @app.route("/connect_user", methods=["POST"])
    def login():
        data = json.loads(request.data.decode("utf8"))
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, status.HTTP_400_BAD_REQUEST
        schema = CredentialsSchema()
        verified_data = schema.load(data)
        user = UserFactory.login(verified_data['username'], verified_data['password'])
        if user:
            token = jwt.encode({
                    "user_id": str(user["_id"]),
                    'iat': int(datetime.now(timezone.utc).timestamp()),
                    'exp': int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp()),
                },
                os.getenv("SECRET_JWT"),
                algorithm="HS256"
            )
            return {
                "data": {
                    "token": token
                }
            }
        
    @app.route('/create_user', methods=['PUT'])
    def create_user():
        data = json.loads(request.data.decode("utf8"))

        id = UserFactory.create(data)
        return jsonify({"data": {'id': str(id)}}), status.HTTP_201_CREATED

    @app.route('/beta/predict_patient', methods=['GET'])
    @can_access_beta_features
    def beta_predict_patient(current_user):
        username = request.args.get('username')

        if username is None:
            return jsonify({'message': {"username": ["Missing data for required field."]}, "error": "Bad Request", "data": None}), status.HTTP_400_BAD_REQUEST
        response = requests.get('http://predict_app_host:5001/predict_patient', params={'username': username})
        if response.status_code == status.HTTP_200_OK:
            return jsonify({"data": response.json()}), response.status_code
        return jsonify(response.json()), response.status_code

    @app.route('/count_patient', methods=['GET'])
    def count_patient():
        args = request.args
        score_args = args.get('score')
        age_args = args.get('age')
        order_args = args.get('order')

        if score_args is None:
            return jsonify({'message': {"score": ["Missing data for required field."]}, "error": "Bad Request", "data": None}), status.HTTP_400_BAD_REQUEST
        
        try:
            score = int(score_args)
        except ValueError:
            return jsonify({'message': {"score": ["Invalid type."]}, "error": "Bad Request", "data": None}), status.HTTP_400_BAD_REQUEST

        if age_args is None:
            count = Patient.count_patient(score)

            return jsonify({"data": {'count': count}}), status.HTTP_200_OK
        else:
            try:
                age = int(age_args)
            except ValueError:
                return jsonify({'message': {"age": ["Invalid type."]}, "error": "Bad Request", "data": None}), status.HTTP_400_BAD_REQUEST
            
            if order_args not in ['lt', 'gt']:
                return jsonify({'message': {"order": ["Invalid value."]}, "error": "Bad Request", "data": None}), status.HTTP_400_BAD_REQUEST

            count = Patient.count_patient(score, age, order_args)

            return jsonify({"data": {'count': count}}), status.HTTP_200_OK
    return app

if __name__=='__main__':
    app = create_app()
    serve(TransLogger(app), host="0.0.0.0", port=5000)

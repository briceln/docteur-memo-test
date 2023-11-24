import json
import os
from flask import Flask, jsonify, request
from flask_api import status
from dotenv import load_dotenv
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import HTTPException
from waitress import serve
from paste.translogger import TransLogger
import sentry_sdk
import logging

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

from models.patient import Patient

def create_app(config = {}):
    load_dotenv()

    sentry_sdk.init(
        dsn="https://7d3de8596a456617d27efe9bddbc9ed9@o1116557.ingest.sentry.io/4506275057500160",
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

    @app.route('/predict_patient', methods=['GET'])
    def predict_patient():
        username = request.args.get('username')

        if username is None:
            return jsonify({'message': {"username": ["Missing data for required field."]}, "error": "Bad Request", "data": None}), status.HTTP_400_BAD_REQUEST

        user = Patient()
        user.get(username)
        user_dict = user.dump()

        prediction = 0
        if user_dict['age'] > 50:
            prediction = user_dict['memory_score'] + 5
        else:
            prediction = user_dict['memory_score'] + 3

        return jsonify({
            'prediction': prediction
        }), status.HTTP_200_OK
    
    return app
        

if __name__=='__main__':
    app = create_app()
    serve(TransLogger(app), host="0.0.0.0", port=5001)
    logger.info('Server listening on port 5001')
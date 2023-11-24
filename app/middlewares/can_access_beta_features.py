from functools import wraps
import os
import jwt
from flask import request
from flask_api import status
from bson.objectid import ObjectId
from models.user import User

def can_access_beta_features(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing",
                "data": None,
                "error": "Unauthorized"
            }, status.HTTP_401_UNAUTHORIZED
        try:
            data = jwt.decode(token, os.getenv("SECRET_JWT"), algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError as e:
            return {
                "message": "Authentication Token has expired",
                "data": None,
                "error": "Unauthorized"
            }, status.HTTP_401_UNAUTHORIZED

        if data['exp'] is None:
            return {
                "message": "Invalid Authentication token",
                "data": None,
                "error": "Unauthorized"
            }, status.HTTP_401_UNAUTHORIZED
        
        current_user = User.get_user_collection().find_one({'_id': ObjectId(data["user_id"])})
        if current_user is None:
            return {
                "message": "Invalid Authentication token",
                "data": None,
                "error": "Unauthorized"
            }, status.HTTP_401_UNAUTHORIZED

        if current_user['status'] == 'healthcare_professionnal' and current_user['type'] in ['neurologist', 'general_practitionner']:
            return f(current_user, *args, **kwargs)
        return {
            "message": "Access Forbidden",
            "data": None,
            "error": "Forbidden"
        }, status.HTTP_403_FORBIDDEN


    return decorated
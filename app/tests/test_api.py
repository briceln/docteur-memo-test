import json
import pytest
from flask_api import status

from app import create_app
from models.user import User

mimetype = 'application/json'

@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        db = User.get_user_collection()
        db.delete_many({})
        db.insert_many([
            {"name":"Albertus","status":"patient","age": 25,"memory_score": 10,"password":"sha256$lJHVtdx2GNjtbCNN$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"},
            {"name":"Roger","status":"patient","age": 20,"memory_score": 15,"password":"sha256$lJHVtdx2GNjtbCNN$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"},
            {"name":"Viktor","status":"patient","age": 30,"memory_score": 20,"password":"sha256$lJHVtdx2GNjtbCNN$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"},
            {"name":"Alexandra","status":"patient","age": 50,"memory_score": 25,"password":"sha256$lJHVtdx2GNjtbCNN$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"},
            {"name":"Bastien","status":"patient","age": 18,"memory_score": 30,"password":"sha256$lJHVtdx2GNjtbCNN$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"},
            {"name":"Jean","status":"patient","age": 26,"memory_score": 24,"password":"sha256$lJHVtdx2GNjtbCNN$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"},
            {"name":"Pierre","status":"patient","age": 24,"memory_score": 27,"password":"sha256$lJHVtdx2GNjtbCNN$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"},
            {"name":"Rémy","status":"patient","age": 28,"memory_score": 28,"password":"sha256$lJHVtdx2GNjtbCNN$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"},
            {"name":"Marie","status":"patient","age": 35,"memory_score": 25,"password":"sha256$lJHVtdx2GNjtbCNN$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"},
            {"name":"Nicolas","status":"patient","age": 32,"memory_score": 17,"password":"sha256$lJHVtdx2GNjtbCNN$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"},
            {"name":"Bart","status":"patient","age": 64,"memory_score": 40,"password":"sha256$lJHVtdx2GNjtbCNN$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"},
            {"name":"Homer","status":"patient","age": 46,"memory_score": 24,"password":"sha256$lJHVtdx2GNjtbCNN$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"},
            {"name":"Marge","status":"patient","age": 40,"memory_score": 25,"password":"sha256$lJHVtdx2GNjtbCNN$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"},
            {"name":"Violetta","status":"caregiver","related_patients":[],"password":"sha256$lJHVtdx2GNjtbCNN$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"},
            {"name":"Markus","status":"healthcare_professionnal","type":"general_practitionner","password":"sha256$lJHVtdx2GNjtbCNN$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"},
            {"name":"Marta","status":"healthcare_professionnal","type":"neurologist","password":"sha256$lJHVtdx2GNjtbCNN$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"},
            {"name":"Iga","status":"healthcare_professionnal","type":"psychologist","password":"sha256$lJHVtdx2GNjtbCNN$ff644d1b5cc413a7c73c24a720412861cb69da1407ca4580f31deb8df6eccee3"}
        ])
        yield client

def test_create_user_with_missing_data(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {}
    response = client.put('/create_user', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content_type == mimetype
    data = {
        "password": "password",
        "status": "healthcare_professionnal",
        "type": "neurologist"
    }
    response = client.put('/create_user', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content_type == mimetype

def test_create_user_with_correct_neurologist_data(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        "username": "pytest",
        "password": "password",
        "status": "healthcare_professionnal",
        "type": "neurologist"
    }
    
    response = client.put('/create_user', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.content_type == mimetype
    assert isinstance(response.json, dict)
    assert set(response.json.keys()) >= {'data'}
    assert isinstance(response.json['data'], dict)
    assert set(response.json['data'].keys()) >= {'id'}
    assert isinstance(response.json['data']['id'], str)

def test_create_user_with_correct_patient_data(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        "username": "pytest",
        "password": "password",
        "status": "patient",
        "age": 34,
        "memory_score": 23
    }
    
    response = client.put('/create_user', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.content_type == mimetype
    assert isinstance(response.json, dict)
    assert set(response.json.keys()) >= {'data'}
    assert isinstance(response.json['data'], dict)
    assert set(response.json['data'].keys()) >= {'id'}
    assert isinstance(response.json['data']['id'], str)

def test_create_user_with_correct_caregiver_data(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        "username": "pytest",
        "password": "password",
        "status": "patient",
        "age": 34,
        "memory_score": 23
    }
    
    response = client.put('/create_user', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.content_type == mimetype
    assert isinstance(response.json, dict)
    assert set(response.json.keys()) >= {'data'}
    assert isinstance(response.json['data'], dict)
    assert set(response.json['data'].keys()) >= {'id'}
    assert isinstance(response.json['data']['id'], str)

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        "username": "pytest_caregiver",
        "password": "password",
        "status": "caregiver",
        "related_patients": [response.json['data']['id']]
    }
    
    response = client.put('/create_user', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.content_type == mimetype
    assert isinstance(response.json, dict)
    assert set(response.json.keys()) >= {'data'}
    assert isinstance(response.json['data'], dict)
    assert set(response.json['data'].keys()) >= {'id'}
    assert isinstance(response.json['data']['id'], str)

def test_create_user_with_wrong_caregiver_data(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        "username": "pytest",
        "password": "password",
        "status": "patient",
        "age": 34,
        "memory_score": 23
    }
    
    response = client.put('/create_user', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.content_type == mimetype
    assert isinstance(response.json, dict)
    assert set(response.json.keys()) >= {'data'}
    assert isinstance(response.json['data'], dict)
    assert set(response.json['data'].keys()) >= {'id'}
    assert isinstance(response.json['data']['id'], str)

    id_user = response.json['data']['id']

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        "username": "pytest_caregiver",
        "password": "password",
        "status": "caregiver",
        "related_patients": [id_user, id_user]
    }
    
    response = client.put('/create_user', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content_type == mimetype

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        "username": "pytest_caregiver",
        "password": "password",
        "status": "caregiver",
        "related_patients": [id_user, '655797df6fb7a59221e58e17']
    }
    
    response = client.put('/create_user', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content_type == mimetype

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        "username": "pytest_caregiver",
        "password": "password",
        "status": "caregiver",
        "related_patients": [id_user, 'not_object_id']
    }
    
    response = client.put('/create_user', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content_type == mimetype


def test_create_user_duplicate(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        "username": "pytest",
        "password": "password",
        "status": "healthcare_professionnal",
        "type": "neurologist"
    }
    
    response = client.put('/create_user', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.content_type == mimetype
    assert isinstance(response.json, dict)
    assert set(response.json.keys()) >= {'data'}
    assert isinstance(response.json['data'], dict)
    assert set(response.json['data'].keys()) >= {'id'}
    assert isinstance(response.json['data']['id'], str)
    response = client.put('/create_user', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content_type == mimetype

def test_count_users_with_memory_score_greater_than_25(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    
    response = client.get('/count_patient?score=25', headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.content_type == mimetype
    assert isinstance(response.json, dict)
    assert set(response.json.keys()) >= {'data'}
    assert isinstance(response.json['data'], dict)
    assert set(response.json['data'].keys()) >= {'count'}
    assert isinstance(response.json['data']['count'], int)
    assert response.json['data']['count'] == 4

def test_count_users_with_memory_score_greater_than_25_and_age_below(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    
    response = client.get('/count_patient?score=25&age=50&order=lt', headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.content_type == mimetype
    assert isinstance(response.json, dict)
    assert set(response.json.keys()) >= {'data'}
    assert isinstance(response.json['data'], dict)
    assert set(response.json['data'].keys()) >= {'count'}
    assert isinstance(response.json['data']['count'], int)
    assert response.json['data']['count'] == 3

def test_connect_user_with_credentials(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        "username": "Albertus",
        "password": "password"
    }
    
    response = client.post('/connect_user', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.content_type == mimetype
    assert isinstance(response.json, dict)
    assert set(response.json.keys()) >= {'data'}
    assert isinstance(response.json['data'], dict)
    assert set(response.json['data'].keys()) >= {'token'}
    assert isinstance(response.json['data']['token'], str)

def test_connect_user_with_wrong_credentials(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        "username": "Albertus",
        "password": "passwor"
    }
    
    response = client.post('/connect_user', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content_type == mimetype

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        "username": "Albertu",
        "password": "password"
    }
    
    response = client.post('/connect_user', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content_type == mimetype

def test_connected_user_access_beta_features_but_does_not_have_access(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        "username": "Albertus",
        "password": "password"
    }
    
    response = client.post('/connect_user', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.content_type == mimetype
    assert isinstance(response.json, dict)
    assert set(response.json.keys()) >= {'data'}
    assert isinstance(response.json['data'], dict)
    assert set(response.json['data'].keys()) >= {'token'}
    assert isinstance(response.json['data']['token'], str)

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer ' + response.json['data']['token']
    }

    data = {
        "username": 'Albertus'
    }
    
    response = client.get('/beta/predict_patient', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.content_type == mimetype

def test_connected_user_access_beta_features(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        "username": "Marta",
        "password": "password"
    }
    
    response = client.post('/connect_user', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.content_type == mimetype
    assert isinstance(response.json, dict)
    assert set(response.json.keys()) >= {'data'}
    assert isinstance(response.json['data'], dict)
    assert set(response.json['data'].keys()) >= {'token'}
    assert isinstance(response.json['data']['token'], str)

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer ' + response.json['data']['token']
    }

    data = {
        "username": 'Albertus'
    }
    
    response = client.get('/beta/predict_patient', query_string=data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.content_type == mimetype
    assert isinstance(response.json, dict)
    assert set(response.json.keys()) >= {'data'}
    assert isinstance(response.json['data'], dict)
    assert set(response.json['data'].keys()) >= {'prediction'}
    assert isinstance(response.json['data']['prediction'], int)
    assert response.json['data']['prediction'] == 13

def test_unauthorize_user_access_beta_features(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        "username": 'Albertus'
    }
    
    response = client.get('/beta/predict_patient', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.content_type == mimetype

def test_expired_user_access_beta_features(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNjU1ZTg3YWJiYjY5NGI0Mzk1ZWEzNWJlIiwiaWF0IjoxNzAwNjkzOTUyLCJleHAiOjE3MDA2OTc1NTJ9.ngfT1CsfOAVOfdQatJFI_TvLzTf4ePzKLC1P0i-YQ90'
    }

    data = {
        "username": 'Albertus'
    }
    
    response = client.get('/beta/predict_patient', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.content_type == mimetype
    assert isinstance(response.json, dict)
    assert set(response.json.keys()) >= {'message', 'error', 'data'}
    assert isinstance(response.json['message'], str)
    assert response.json['message'] == 'Authentication Token has expired'

def test_unknown_api_route(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.get('/user', headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.content_type == mimetype

def test_sending_empty_data(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    response = client.post('/connect_user', headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content_type == mimetype
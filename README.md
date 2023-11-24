### REQUIREMENTS

- Docker ([https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/))
- Docker-compose ([https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/))

### RUN SERVICES

```bash
$ docker-compose build
```
```bash
$ docker-compose up
```

The REST API can be accessed at the following address: [http://127.0.0.1:5000](http://127.0.0.1:5000)

In this mode, the second API with /predict_patient endpoint and mongoDB are not accessible from the outside.

### RUN API TESTS AND COVERAGE

```bash
$ docker-compose -f docker-compose_test.yml build
```
```bash
$ docker-compose -f docker-compose_test.yml up
```

The result of the coverage can be seen by opening the page **index.html** inside **htmlcov** folder.

In this mode, all APIs and mongoDB are accessible from the outside.

### API DOCUMENTATION

```
PUT create_user`
Parameters :
- username = string : name of the user
- password = string : user password
- status = string : user status (caregiver, patient, ...)
- different args depending on the type of user (type of healthcare professionnal, ...)

Response : 
{
    "data": {
        "id": "6560a29967cb0de766dbd84f"
    }
}
```

```
POST connect_user`
Parameters :
- username = string : name of the user
- password = string : user password

Response : 
{
    "data": {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNjU2MGEyOTk2N2NiMGRlNzY2ZGJkODRmIiwiaWF0IjoxNzAwODMxOTk1LCJleHAiOjE3MDA4MzU1OTV9.PU-VRzfwMR4lLbL3DjUT5RD5TeZQA8Xvm-kQJleOkDY"
    }
}
```

```
GET count_patient`
Parameters :
- score = int : cut-off value for memory_score
- age (optionnal) = int : cut-off value for age
- order (optionnal) = ['gt', 'lt'] : higher or lower than age cut-off value

Response : 
{
    "data": {
        "count": 1
    }
}
```

```
GET beta/predict_patient`
Headers:
- Authorization : Bearer token
Parameters :
- username = string : patient name

Response : 
{
    "data": {
        "prediction": 13
    }
}
```

### USEFUL INFORMATION

#### DATABASE CREDENTIALS
The database connection credentials are in the .env file located at the root of /app.  

#### DEFAULT USER PASSWORD
The default user password is 'password'.

#### DUPLICATE OF MODELS AND SCHEMA PACKAGES
**Unfortunately, the python package containing the models/ and schema/ folders when copied into the docker was not detected by python, which is why a copy is included in app/ and predict_app/. One solution would be to import the package via a github repo to get around the problem.**

#### WHY SENTRY
[Sentry](https://sentry.io/) is used to monitor the performance (p50, p99, TPM) of each route and track errors.

![Sentry_api](./img/sentry_api.png)
![Sentry_api_test_features](./img/sentry_feature_test.png)
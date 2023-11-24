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

### USEFUL INFORMATION

The database connection credentials are in the .env file located at the root of /app.  

[Sentry](https://sentry.io/) is used to monitor the performance of each route and track errors.

![Sentry_api](./img/sentry_api.png)
![Sentry_api_test_features](./img/sentry_feature_test.png)
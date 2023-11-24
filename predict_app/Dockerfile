FROM python:3.6
RUN  python3.6 -m pip install --upgrade pip
WORKDIR /predict_app
ADD ./requirements.txt /predict_app/requirements.txt
RUN pip install -r requirements.txt
ADD . /predict_app
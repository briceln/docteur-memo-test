FROM python:3.6
RUN  python3.6 -m pip install --upgrade pip
WORKDIR /app
ADD ./app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD ./app /app

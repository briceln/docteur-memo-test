FROM python:3.6
WORKDIR /app
RUN python3.6 -m pip install --upgrade pip
ADD app/requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
ADD ./app ./
ADD ./shared_package ./shared_package
ENV PYTHONPATH "${PYTHONPATH}:/app/shared_package"
FROM python:3.6
RUN  python3.6 -m pip install --upgrade pip
WORKDIR /predict_app
ADD predict_app/requirements.txt /predict_app/requirements.txt
RUN pip install -r requirements.txt
ADD ./predict_app ./
ADD ./shared_package ./shared_package
ENV PYTHONPATH "${PYTHONPATH}:/predict_app/shared_package"
RUN ls
RUN ls -R *
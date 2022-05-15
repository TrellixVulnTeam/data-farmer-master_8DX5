FROM python:3.9.12-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./app ./app
COPY ./base_dockerfile ./base_dockerfile
COPY ./run.py .

CMD [ "python3", "run.py"]

# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /botrk_back

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install dirsearch
RUN apt-get update
RUN apt-get -y install sqlmap
EXPOSE 5000:5000

COPY . .

CMD [ "python", "-m" , "flask", "--app", "flaskr", "run", "--host=0.0.0.0"]
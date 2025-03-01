FROM python:3.13.2-alpine

WORKDIR /app

ADD . /app

RUN pip install pipenv && pipenv install --system

CMD ["./start.sh"]
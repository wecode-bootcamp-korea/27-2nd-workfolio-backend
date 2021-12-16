FROM ubuntu:20.04

WORKDIR /usr/src/app

COPY requirements/requirements.txt ./

RUN apt-get update -y \
    && apt-get install software-properties-common -y \
    && add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get install python3 python3-pip libmysqlclient-dev -y

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:80", "--timeout", "600", "workfolio.wsgi:application"]

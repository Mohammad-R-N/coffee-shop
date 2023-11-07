FROM python:3.10

WORKDIR /src

COPY requirements.txt /src/

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /src/
EXPOSE 8000

CMD [ "gunicorn","config.wsgi",":8000" ]
FROM python:3.10

COPY . /var/www/app

WORKDIR /var/www/app

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]
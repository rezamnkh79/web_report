FROM python:3.8.3-alpine

# set work directory
WORKDIR /home/ubuntu/Desktop/django/MAP


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /home/ubuntu/Desktop/django/MAP
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "127.0.0.0:8000"]
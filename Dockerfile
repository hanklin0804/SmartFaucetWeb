FROM python:3.9.10-slim

WORKDIR /backend
# ENV /backend /home/
ENV PYTHONBUFFERED 1
COPY ./requirements.txt /backend/requirements.txt

RUN apt-get -qq update \ 
    && apt-get upgrade -y \
    && apt-get install -y gcc build-essential default-libmysqlclient-dev \
    && pip install --no-cache-dir -r requirements.txt

COPY ./backend /backend
ENTRYPOINT ["/backend/entrypoint.sh"]


# RUN python manage.py collectstatic --noinput
# EXPOSE 8080
# CMD ['gunicorn', '--bind', '0.0.0.0:8080', 'project_name.wsgi:application']

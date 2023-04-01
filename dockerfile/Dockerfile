FROM python:3.9.10-slim
MAINTAINER Flaky

WORKDIR /workdir
# ENV /backend /home/

# pip freese > requirements.txt
COPY requirements.txt .

# RUN apt-get -qq update \ 
#     && apt-get upgrade -y \
#     && apt-get install -y 
RUN pip insatll --no-cache-dir -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput


EXPOSE 8080

CMD ['gunicorn', '--bind', '0.0.0.0:8787', 'project_name.wsgi:application']

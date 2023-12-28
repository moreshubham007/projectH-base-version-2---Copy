# FROM python:3.8-slim-buster
# LABEL maintainer="shubhammore007@outlook.com"

# COPY . .
# RUN ls
# RUN pip install virtualenv
# RUN python3 -m venv env


# RUN pip install -r dependencies.txt
# # RUN python manage.py makemigrations
# # RUN python manage.py migrate
# # RUN python manage.py migrate --run-syncdb
# EXPOSE 8000
# CMD ["bash", "-c", "source /app/env/bin/activate && python manage.py runserver 0.0.0.0:8000"]


# #

FROM python:3.9-slim-buster
LABEL maintainer="shubhammore007@outlook.com"
WORKDIR /
RUN command apt-get update
COPY . .
RUN pip install -r dependencies.txt
EXPOSE 8000
CMD ["python3","manage.py","runserver","0.0.0.0:8000"]



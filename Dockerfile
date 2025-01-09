# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/boorish

COPY ./boorish /usr/src/boorish 

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt update && apt -y install pkg-config
RUN apt-get install -y netcat
RUN apt -y install libmariadb-dev
RUN apt-get install -y gcc
RUN apt-get install -y imagemagick
RUN apt-get install -y ffmpeg


RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/boorish/entrypoint.sh
RUN chmod +x /usr/src/boorish/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/boorish/entrypoint.sh"]

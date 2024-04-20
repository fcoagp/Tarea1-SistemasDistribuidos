FROM python:3.8-slim-buster
ARG CACHE_TYPE=CENTRAL
WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
ENV CACHE_TYPE $CACHE_TYPE
ENV GRPC_SERVER $GRPC_SERVER
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
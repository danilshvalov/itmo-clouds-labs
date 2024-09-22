FROM ubuntu:latest

WORKDIR /app
COPY ./ /app

RUN apt-get update && apt-get -y install python3 ssh vim

CMD ["/app/start.sh"]

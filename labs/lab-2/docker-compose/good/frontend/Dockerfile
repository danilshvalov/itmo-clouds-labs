FROM python:3.12.6

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY ./ /home/appuser

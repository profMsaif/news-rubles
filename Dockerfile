FROM python:3.8-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="/$VIRTUAL_ENV/bin:$PATH"

WORKDIR /www
EXPOSE 8000
COPY req.txt /www/req.txt

RUN pip install -r req.txt

COPY . /www/
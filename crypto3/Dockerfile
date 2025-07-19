FROM python:3.12.2-alpine3.19

EXPOSE 5000

WORKDIR /app

RUN apk add --no-cache socat
RUN apk add --no-cache --virtual .build-deps build-base

RUN pip install --trusted-host pypi.python.org pycryptodome
RUN apk del .build-deps

COPY chal.py /app

USER nobody

ENTRYPOINT socat tcp-l:5000,reuseaddr,fork EXEC:"python chal.py",pty,stderr,echo=0

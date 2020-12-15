FROM python:3.8-slim
LABEL maintainer="Igor Nehoroshev <hi@neigor.me>"

COPY . /app/kolombo
COPY docker/auth/requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt \
    && mkdir /etc/kolombo \
    && find kolombo -type d -name __pycache__ -exec rm -r {} \+
# Volume should be attached to /etc/kolombo
COPY docker/auth/kolombo.conf /etc/kolombo/kolombo.env
EXPOSE 7089/tcp
CMD uvicorn kolombo:api --loop=uvloop --host=0.0.0.0 --port=7089

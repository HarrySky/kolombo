FROM nginx:mainline-alpine
LABEL maintainer="Igor Nehoroshev <hi@neigor.me>"

RUN apk add --no-cache nginx-mod-mail && mkdir /etc/nginx/mail-enabled
COPY docker/nginx/nginx.conf /etc/nginx/nginx.conf
COPY docker/nginx/server.crt /etc/ssl/certs/server.crt
COPY docker/nginx/server.key /etc/ssl/certs/server.key
EXPOSE 25/tcp 587/tcp 993/tcp

FROM nginx:mainline-alpine
LABEL maintainer="Igor Nehoroshev <hi@neigor.me>"

RUN apk add --no-cache nginx-mod-mail && mkdir /etc/nginx/mail-enabled
COPY docker/nginx/nginx.conf /etc/nginx/nginx.conf
EXPOSE 587/tcp 993/tcp

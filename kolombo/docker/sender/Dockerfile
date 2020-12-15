FROM alpine:3.12
LABEL maintainer="Igor Nehoroshev <hi@neigor.me>"

ARG TIMEZONE=Europe/Tallinn

COPY docker/sender/rsyslog.conf /etc/rsyslog.conf
COPY docker/sender/gen_key.sh /bin/gen_key
COPY docker/sender/startup.sh /bin/startup

# Install needed software
RUN apk add --no-cache rsyslog postfix opendkim opendkim-utils tzdata \
# Add postfix to opendkim group
    && addgroup postfix opendkim \
# Set timezone
    && ln -sf /usr/share/zoneinfo/${TIMEZONE} /etc/localtime \
    && echo "${TIMEZONE}" > /etc/timezone

# Copy configurations
COPY docker/sender/postfix.conf /etc/postfix/main.cf
COPY docker/sender/opendkim.conf /etc/opendkim/opendkim.conf

# Create aliases, so that Postfix stop giving warnings
RUN touch /etc/postfix/aliases && newaliases
# Set up OpenDKIM
RUN mkdir -p /run/opendkim /etc/opendkim/keys \
    && chown opendkim:postfix /run/opendkim \
    && chown -R opendkim:opendkim /etc/opendkim \
    && chmod -R go-wrx /etc/opendkim/keys \
    && chown opendkim:opendkim /etc/opendkim/opendkim.conf

# 25 for SMTP (send)
EXPOSE 25/tcp
ENTRYPOINT ["/bin/startup"]

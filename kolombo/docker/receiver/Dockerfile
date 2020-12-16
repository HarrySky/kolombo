FROM alpine:3.12
LABEL maintainer="Igor Nehoroshev <hi@neigor.me>"

ARG TIMEZONE=Europe/Tallinn

COPY docker/receiver/rsyslog.conf /etc/rsyslog.conf
# Volume should be attached to /etc/postfix/virtual
COPY docker/receiver/virtual-domains /etc/postfix/virtual/domains
COPY docker/receiver/virtual-addresses /etc/postfix/virtual/addresses
COPY docker/receiver/virtual-mailbox /etc/postfix/virtual/mailbox

# Install needed software
RUN apk add --no-cache rsyslog postfix dovecot tzdata openssl \
# Set timezone
    && ln -sf /usr/share/zoneinfo/${TIMEZONE} /etc/localtime \
    && echo "${TIMEZONE}" > /etc/timezone \
# Generate SSL certificates
    && openssl req -x509 -nodes -newkey rsa:4096 -keyout /etc/postfix/tls.key -out /etc/postfix/tls.crt -days 1825
# Copy script that "checks password" (just returns OK, check MUST be on nginx level)
COPY docker/receiver/checkpassword.sh /bin/checkpassword
# Copy configurations
COPY docker/receiver/dovecot.conf /etc/dovecot/dovecot.conf
COPY docker/receiver/postfix.conf /etc/postfix/main.cf
# Create aliases, so that Postfix stop giving warnings
RUN touch /etc/postfix/aliases && newaliases

# 25 for SMTP (receive), 143 for IMAP
EXPOSE 25/tcp 143/tcp
CMD postmap /etc/postfix/virtual/addresses \
    && postmap /etc/postfix/virtual/mailbox \
    && chgrp -R postfix /etc/postfix/virtual \
    && postfix start && dovecot && rsyslogd -n

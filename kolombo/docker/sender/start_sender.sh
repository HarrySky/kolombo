#!/bin/sh
set -e

if [ -z "$1" ] ; then
    echo "No arguments supplied, provide DOMAIN to start normally"
    exit 1
fi

if [ ! -f "/etc/opendkim/keys/${1}" ] ; then
    echo "DKIM key does not exist! Generate one via 'kolombo dkim generate ${1}'"
    exit 2
fi

chown -R opendkim:opendkim /etc/opendkim/keys
sed -i -e "s/doma.in/${1}/g" /etc/postfix/main.cf
sed -i -e "s/doma.in/${1}/g" /etc/opendkim/opendkim.conf
chmod 640 /etc/postfix/main.cf

opendkim
postfix start
exec rsyslogd -n

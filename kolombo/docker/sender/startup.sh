#!/bin/sh
set -e

if [ -z "$1" ] ; then
    echo "No arguments supplied, arguments usage:"
    echo "- 'DOMAIN' to start normally"
    echo "- 'gen_key DOMAIN' to generate DKIM key for domain"
    exit 1
fi

if [ "$1" == "gen_key" ] ; then
    /bin/gen_key "${2}"
    exit 0
fi

if [ ! -f "/etc/opendkim/keys/${1}" ] ; then
    echo "DKIM key does not exist! Generate one"
    exit 2
fi

chown -R opendkim:opendkim /etc/opendkim/keys
sed -i -e "s/doma.in/${1}/g" /etc/postfix/main.cf
sed -i -e "s/doma.in/${1}/g" /etc/opendkim/opendkim.conf

opendkim
postfix start
rsyslogd -n

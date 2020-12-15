#!/bin/sh
set -e

if [ -z "$1" ] ; then
    echo "No domain argument provided"
    exit 1
fi

cd /etc/opendkim/keys
opendkim-genkey -b 2048 -d ${1} -s mail -v
chown opendkim:opendkim mail.private
mv mail.private ${1}
mv mail.txt ${1}.txt

echo "TXT record for mail._domainkey.${1}"
cat ${1}.txt

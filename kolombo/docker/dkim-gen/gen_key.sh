#!/bin/sh
set -e

if [ -z "$1" ] ; then
  echo "Provide domain as first argument"
  exit 1
fi

opendkim-genkey -b 2048 -d ${1} -s mail -v
mv mail.private ${1}
mv mail.txt ${1}.txt
chown opendkim:opendkim ${1}

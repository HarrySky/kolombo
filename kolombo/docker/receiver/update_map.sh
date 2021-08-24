#!/bin/sh
set -e

postmap /etc/postfix/virtual_files/addresses
postmap /etc/postfix/virtual_files/mailbox
postmap -oF lmdb:/etc/postfix/virtual_files/ssl_map

chmod -R 640 /etc/postfix/virtual_files
chmod 750 /etc/postfix/virtual_files
chown -R root:postfix /etc/postfix/virtual_files

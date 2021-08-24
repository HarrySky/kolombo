#!/bin/sh

/bin/update_map
chgrp -R 1000 /var/mail
chmod 770 /var/mail
chmod 640 /etc/postfix/main.cf

postfix start
dovecot
exec rsyslogd -n

#!/bin/sh

# Since nginx checks auth - no need to do it on Dovecot level
read -d $'\x0' -r -u 3 USER
read -d $'\x0' -r -u 3 PASS
export password="{PLAIN}$PASS"
export EXTRA="password $EXTRA"
exec $1

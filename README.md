# Kolombo

![Kolombo Logo](https://raw.githubusercontent.com/HarrySky/kolombo/main/logo.png "Kolombo Logo")

CLI for easy mail server managing 💌

**NB! Work in progress, not ready for production use!**

## Introduction

What Kolombo does:
- Configures email domains (`example.com/mx.example.com`) and users (`info@example.com`)
- Generates DKIM keys with TXT records to add to DNS
- Manages all services needed for email to work in docker-compose

## Installation

Python 3.8+, sudo, Docker and docker-compose should be installed on system.

Install with pip:
```sh
pip install kolombo
```

## How to use

Documentation is coming, for now,
this is how to setup mail server for
domain `example.com` with user `info@example.com`

```sh
# Initialize Kolombo
kolombo init

# Add domain and generate DKIM keys for it
kolombo domain add example.com mx.example.com  # MX field is optional
kolombo dkim generate example.com  # generates DKIM keys and returns DNS TXT record to add
kolombo dkim txt example.com  # returns DNS TXT record to add

# Add user (email) for domain you just added
kolombo user add info@example.com

# Deploy Kolombo services and senders one by one...
kolombo run receiver  # Listens on 25 for incoming mail, gives emails to users that come through nginx 993/995 ports
kolombo run auth  # Authenticates SMTP/POP3/IMAP users from nginx
kolombo run nginx  # Listens on 465 (SMTP), 993 (IMAP) and 995 (POP3)
kolombo run senders  # Send emails from users that come through nginx 465 port

# ... or deploy all everything at once
kolombo run all

# Stop all Kolombo services and senders
kolombo stop all

# ... or stop them one by one
kolombo stop receiver
kolombo stop auth
kolombo stop nginx
kolombo stop senders
```

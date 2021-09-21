# Initialization

First of all you need to initialize Kolombo by running following command:

```sh
kolombo init
```

It will create `/etc/kolombo` files and install autocompletion.

Command is **interactive** and will ask for your input during setup.

# Managing domains

You can manage domains that mail server will be dealing with via `kolombo domain`.

## Adding domains

You can add domain via `kolombo domain add` like that:

```sh
kolombo domain add example.com
```

It assumes that **example.com** domain either has no MX record, or has MX record **example.com**. If you need to **specify MX** record - you can use optional MX argument like that:

```sh
kolombo domain add example.com mx.example.com
```

**NB!** Kolombo will use MX domain's LetsEncrypt certificates for TLS encrypted communication.

# DKIM keys

You can manage DKIM keys for added domains via `kolombo dkim`.

## Generating DKIM keys

You can generate DKIM keys via `kolombo dkim generate` like that:

```sh
kolombo dkim generate example.com
```

This command will return **TXT record that you will need to add to DNS**.

**NB!** If DKIM keys already exist - they will be overwritten by new ones.

## Read DNS TXT record for DKIM

You can read DNS TXT record for existing DKIM keys via `kolombo dkim txt` like that:

```sh
kolombo dkim txt example.com
```

# Managing users

You can manage users that mail server will be dealing with via `kolombo user`.

## Adding users

You can add user via `kolombo user add` like that:

```sh
kolombo user add info@example.com
```

Command is **interactive** and will ask for password input.

# Kolombo services

Kolombo has following services:

* **receiver**
    * listens on host's port 25 for incoming *SMTP* mail
    * gives email via *POP3*/*IMAP* to authenticated users
* **auth**
    * authenticates users coming from **nginx**
* **nginx**
    * listens on host's port 465 for outgoing *SMTP* mail
    * listens on host's port 993 for *IMAP* requests
    * listens on host's port 995 for *POP3* requests
* **sender**
    * sends outgoing email via *SMTP* from authenticated users

## Deploying services

You can deploy services via `kolombo run`.

Commands will build service image and start service.

### Deploying everything at once

You can deploy all Kolombo services and senders at once like that:

```sh
kolombo run all
```

### Deploying one by one

You can deploy services one by one via `kolombo run SERVICE` like that:

```sh
kolombo run receiver
kolombo run auth
kolombo run nginx
kolombo run senders
```

This way you can update service when Kolombo was updated.

## Stopping services

You can stop services via `kolombo stop`.

### Stopping everything at once

You can stop all Kolombo services and senders at once like that:

```sh
kolombo stop all
```

### Deploying one by one

You can stop services one by one via `kolombo stop SERVICE` like that:

```sh
kolombo stop receiver
kolombo stop auth
kolombo stop nginx
kolombo stop senders
```

You don't need to do it for update, as `kolombo run SERVICE` recreates service if it is already running

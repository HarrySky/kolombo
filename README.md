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

## Documentation

Documentation is at https://docs.neigor.me/kolombo/

For quick start see https://docs.neigor.me/kolombo/quickstart/

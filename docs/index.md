<p align="center">
  <img width="240px" src="./img/logo.png" alt='Kolombo Logo'>
</p>
<p align="center">
💌 <em>CLI for easy mail server managing</em> 💌
</p>

---

<p align="center">
<a href="https://pypi.org/project/kolombo">
    <img src="https://img.shields.io/pypi/v/kolombo" alt="PyPI: kolombo">
</a>
<a href="https://github.com/ambv/black">
    <img src="https://img.shields.io/badge/code_style-black-000000.svg" alt="Code Style: Black">
</a>
</p>

---

# Introduction

Kolombo is a CLI for managing mail server (setting up domains and users, updating, etc)

Project is in beta, it gives you the following:

* Email server configuration and management in few commands
* 100% type annotated codebase

## Requirements

Python 3.8+, [sudo](https://www.sudo.ws), [Docker](https://docs.docker.com/engine/install) and [docker-compose](https://docs.docker.com/compose/install)

## Installation

Install Kolombo with pip (**please pin your dependency**):
```shell
$ pip install kolombo==0.5.0
```

## Dependencies

Kolombo CLI requires following dependencies:

* **typer** (with **click** 8.x) - for CLI
* **shellingham** - for shell detection
* **rich** - for rich console output
* **docker** - for working with Docker API
* **ormar** (with **aiosqlite**) - for working with data
* **cryptography** - for passwords hashing
* **importlib-resources** - `importlib.resources` backport (*for Python version < 3.9*)


<p align="center">&mdash; 💌 &mdash;</p>
<p align="center"><i>Kolombo is <a href="https://github.com/HarrySky/kolombo/blob/main/LICENSE">Apache 2.0 licensed</a> code.</i></p>

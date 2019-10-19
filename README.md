# Public IP Address Check (with *[ipify][ipify]* and *[IFTTT][ifttt]*)

## Overview

This project aims to automate public IP address checking and alert via *[IFTTT][ifttt]* when a change happens.

## Usage

After installing [dependencies](#requirements) and [configuring](#setup) *[IFTTT][ifttt]* and [`config.yaml`](config.yaml.example), run [`process.py`](process.py).

## Requirements

This code is designed around the following:

- Python 3
    - `requests`
        - `GET` with *[ipify][ipify]*
        - `POST` with *[IFTTT][ifttt]*
    - `pyyaml` for managing configuration
    - other [requirements](requirements.txt) 

## Setup

1. Setup with *[IFTTT][ifttt]*.
2. Create a new applet.
3. For **"this"**, choose "Webhooks".
4. Choose an **Event Name**.
    - Store this into [`config.yaml`](config.yaml.example) in `event`.
5. Pick an appropriate destination for **"that"**, e.g. "Email".
6. Save the applet after you've filled everything per your desire.
7. Retrieve your personal URL from [here](https://ifttt.com/maker_webhooks/settings).
    - Store the part after `https://maker.ifttt/use/` into [`config.yaml`] in `url`.

## Project Files

- [`config.yaml.example`](config.yaml.example)
    - template configuration; copy to `config.yaml` and follow [setup](#setup)
- [`ipaddr.yaml.example`](ipaddr.yaml.example)
    - a literal example file; do not use or manipulate this
    - `ipaddr.yaml` will be automatically created and subsequently reused by [`process.py`](process.py)
- [`process.py`](process.py)
    - the script for this project
- [`config.py`](config.py)
    - configuraton handler
- [`ifttt.py`](ifttt.py)
    - *[IFTTT][ifttt]* handler
- [`ipaddr.py`](ipaddr.py)
    - IP address retriever; currently retrieves via *[ipify][ipify]*

## Disclaimer

This project is not affiliated with or endorsed by *[ipify][ipify]* or *[IFTTT][ifttt]*. See [`LICENSE`](LICENSE) for more detail.

[ipify]: https://ipify.org
[ifttt]: https://ifttt.com

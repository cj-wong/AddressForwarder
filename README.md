# Public IP Address Check (with *[ipify][ipify]* and *[Cloudflare][cloudflare]*)

## Overview

This project aims to automate public IP address checking. When a change happens, the scripts will attempt to adjust *[Cloudflare][cloudflare]* DNS settings and optionally alert via *[IFTTT][ifttt]*.

## Branches

- `master`
- `cloudflare`
    - for use with *[Cloudflare][cloudflare]*

## Usage

After installing [dependencies](#requirements) and [configuring](#setup) *[Cloudflare][cloudflare]* and [`config.yaml`](config.yaml.example), run [`process.py`](process.py).

## Requirements

This code is designed around the following:

- Python 3
    - `requests`
        - `GET` with *[ipify][ipify]*
        - *(optional)* `POST` with *[IFTTT][ifttt]*
    - `python-cloudflare` for using the *Cloudflare* API
    - `pyyaml` for managing configuration
    - other [requirements](requirements.txt) 

## Setup

1. Setup with *[Cloudflare][cloudflare]*.
2. Go to **"Get your API token"** on your domain overview page.
3. Pick one of the options below:
    - **API Key**
        - View your **"Global API Key"**. You must use your e-mail address registered to *Cloudflare*.
    - **API Token**
        - Create a token. Set permissions as you like; this token should be able to *edit* the intended zone (domain).
4. Record your **Zone ID**.
5. Configure [`config.yaml`](config.yaml.example), including filling out any/all subdomains you wish to update.

### (optional) *[IFTTT][ifttt]*

1. Setup with *IFTTT*.
2. Create a new applet.
3. For **"this"**, choose "Webhooks".
4. Choose an **Event Name**.
    - Store this into [`config.yaml`](config.yaml.example) in `event`.
5. Pick an appropriate destination for **"that"**, e.g. "Email".
6. Save the applet after you've filled everything per your desire.
7. Retrieve your personal URL from [here](https://ifttt.com/maker_webhooks/settings).
    - Store the part after `https://maker.ifttt/use/` into [`config.yaml`](config.yaml.example) in `url`.

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
- [`cloudflare.py`](cloudflare.py)
    - *[Cloudflare][cloudflare]* handler
- [`ifttt.py`](ifttt.py)
    - *[IFTTT][ifttt]* handler
- [`ipaddr.py`](ipaddr.py)
    - IP address retriever; currently retrieves via *[ipify][ipify]*

## Disclaimer

This project is not affiliated with or endorsed by *[ipify][ipify]* or *[IFTTT][ifttt]*. See [`LICENSE`](LICENSE) for more detail.

[ipify]: https://ipify.org
[ifttt]: https://ifttt.com
[cloudflare]: https://www.cloudflare.com

# I've Moved

## Overview

Ever want to know when your WAN IP address changes? You can now with *I've Moved!* This project automates WAN IP address checking using *[ipify][IPIFY]* and alerts via *[IFTTT][IFTTT]* when a change happens. This project is helpful for monitoring dynamic WAN IP addresses. If *[Cloudflare][CLOUDFLARE]* configuration is added, the project will also automate updates to the DNS entries of your subdomains.

### Caveats

Only IPv4 is supported. Consequently for *Cloudflare* functionality, only `A` records are supported.

## Usage

After installing [dependencies](#requirements) and [configuring](#setup) *[IFTTT][IFTTT]*, optionally *[Cloudflare][CLOUDFLARE]*, and [config.yaml](config.yaml.example), run [main.py](main.py).

## Requirements

This code is designed around the following:

- Python 3
    - `requests`
        - `GET` with *[ipify][IPIFY]*
        - `POST` with *[IFTTT][IFTTT]*
        - *(optional)* `PUT` with *[Cloudflare][CLOUDFLARE]*
    - `pyyaml` for managing configuration
    - other [requirements](requirements.txt)

## Setup *[IFTTT][IFTTT]*

0. Setup with *IFTTT* by creating an account.
1. [Create](https://ifttt.com/create) a new applet.
2. For **"This"**, choose "Webhooks".
3. Choose an **Event Name**. Store this into [config.yaml](config.yaml.example) in `event`.
4. Pick an appropriate destination for **"That"**, e.g. "Email".
5. Save the applet after you've filled everything per your desire.
6. Retrieve your personal URL from your [webhooks](https://ifttt.com/maker_webhooks/settings) page. Record the part after `https://maker.ifttt/use/` in the configuration into `url`.

### (optional) Setup *[Cloudflare][CLOUDFLARE]*

0. Setup with *Cloudflare*. This means adding your domain and all other subdomains to your DNS records. Your domain goes into `domain` in the configuration.
1. On your domain overview page, record your **"Zone ID"** (in the sidebar, under **"API"**) in the configuration into `zone`.
2. Go to **"Get your API token"** (also in the **"API"** section) on the same overview page.
3. Pick one of the options below. *Do not use both.*

    - **API Token** *(recommended)*
        - **Create** a token. Set permissions as you like; at the minimum, this token should be able to *edit* the intended zone (domain). Record the token into `token` in the configuration.
        - Example permissions: `Zone Settings:Read, Zone:Read, DNS:Edit`

    - **API Key**
        - **View** your **"Global API Key"**. You must use your e-mail address registered to *Cloudflare*. Record both the e-mail address and key into `email` and `key` in the configuration, respectively.

4. Configure [config.yaml](config.yaml.example), filling out any/all subdomains you wish to update. For the base domain (no `www`), use the empty string `''`. You may choose to run `python cloudflare.py` to save subdomain identifiers, as they are necessary for updates. 

## Project Files

- [config.yaml.example](config.yaml.example)
    - template configuration; copy to `config.yaml` and follow [setup](#setup)
- [ipaddr.yaml.example](ipaddr.yaml.example)
    - a literal example file; do not use or manipulate this
    - `ipaddr.yaml` will be automatically created and subsequently reused by [main.py](main.py)
- [main.py](main.py)
    - the script for this project
- [config.py](config.py)
    - configuraton handler
- [cloudflare.py](cloudflare.py)
    - *[Cloudflare][CLOUDFLARE]* handler
- [ifttt.py](ifttt.py)
    - *[IFTTT][IFTTT]* handler
- [ipaddr.py](ipaddr.py)
    - IP address retriever; currently retrieves via *[ipify][IPIFY]*

## Disclaimer

This project is not affiliated with or endorsed by *[ipify][IPIFY]*, *[IFTTT][IFTTT]*, or *[Cloudflare][CLOUDFLARE]*. See [LICENSE](LICENSE) for more detail.

[IPIFY]: https://ipify.org
[IFTTT]: https://ifttt.com
[CLOUDFLARE]: https://www.cloudflare.com

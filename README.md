# AddressForwarder

## Overview

AddressForwarder will check your public IP address per run. When your address has changed, it will update your Cloudflare DNS records so that your domain and subdomains can be accessible even with a dynamic IP address. AddressForwarder can also alert via webhook after a change was made. Originally, only IFTTT was supported, but with the 2.0.0 update, general webhooks are supported.

AddressForwarder is best run with `cron` or other similar scheduling software, so that changes are monitored passively. A period of 5 minutes is good enough for this purpose; any shorter and you may risk being banned from the services that this program relies to get IP address.

## Usage

You need to have [Cloudflare] setup for your domain(s). Afterwards, follow the [setup](#setup-cloudflare) below.

## Requirements

This code was tested with the following:

- Python 3.9
    - `requests`
    - other [requirements](requirements.txt)

`pyyaml` was a requirement until the 2.0.0 update.

### Setup *[Cloudflare][CLOUDFLARE]*

1. On your domain overview page after selecting a domain, copy your **"Zone ID"** (in the sidebar, under **"API"**) in the configuration into `zone`.
2. Go to **"Get your API token"** (also in the **"API"** section) on the same overview page.
3. Pick one of the options below. ***Do not use both.***

    - **API Token** *(recommended)*
        - **Create** a token. Set permissions as you like; at the minimum, this token should be able to *edit* the intended zone (domain). Record the token into `token` in the configuration.
        - Example permissions: `Zone Settings:Read, Zone:Read, DNS:Edit`

    - **API Key**
        - **View** your **"Global API Key"**. You must use your e-mail address registered to *Cloudflare*. Record both the e-mail address and key into `email` and `key` in the configuration, respectively.

4. [Configure](#configuration) `config.json`.

## Configuration

See `config.json.example` for more information.

The top-level `"cloudflare"` block pertains to solely Cloudflare; the fields are detailed above. Subdomains go under `"subdomains"`, a list, and must contain the fields `"subdomain"`, `"identifier"`, and `"proxied"` (boolean).

For webhooks, a list of webhooks can be used. `"url"` is where the `"message"` will be `POST`ed. `"message"` can be either a string or a dictionary/JSON object. If you'd like to include the changed IP address in the message, you can make the message a Python pre-formatted string by using `{ipv4}` and/or `{ipv6}`, e.g. `Your new IP address: {ipv4}/{ipv6}`. Note that messages are per webhook and not universally defined.

If you're upgrading from version 1.2.5 to 2.0.0, you can convert the previous hard-coded [IFTTT][IFTTT] configuration, change the webhook URL to `https://maker.ifttt.com/trigger/{ifttt.event}/with/key/{ifttt.url}/`, where the values `ifttt.event` and `ifttt.url` correspond below in the old YAML format:

```
ifttt:
  url: ifttt.url
  event: ifttt.event
```

Or you can run `python utils/2.0.0-migration/migrate.py` before removing the previous environment to convert the prior YAML to the new JSON configuration.

## Disclaimer

This project is not affiliated with or endorsed by the APIs used in `AddressForwarder.ipaddr`, *[IFTTT][IFTTT]*, or *[Cloudflare][CLOUDFLARE]*. See [LICENSE](LICENSE) for more detail.

[IFTTT]: https://ifttt.com
[CLOUDFLARE]: https://www.cloudflare.com

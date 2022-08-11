import json
from pathlib import Path

import yaml


# Ensure that this script runs in the project root.
p = Path('.').resolve()
if "2.0.0-migration" in str(p):
    p = (p / '..').resolve()
if "utils" in str(p):
    p = (p / '..').resolve()

with (p / 'config.yaml').open() as f:
    old = yaml.safe_load(f)

new = {}

if 'cloudflare' in old:
    new['cloudflare'] = {
        key: value for key, value in old['cloudflare'].items()
        if key != 'subdomains'
        }
    subdomains = []
    for subdomain, params in old['cloudflare']['subdomains'].items():
        params['subdomain'] = subdomain
        subdomains.append(params)
    new['cloudflare']['subdomains'] = subdomains

ifttt_url = 'https://maker.ifttt.com/trigger'
ifttt_id = old['ifttt']['url']
ifttt_event = old['ifttt']['event']
default_message = {'value1': "{ipaddr}"}
ifttt_wh_url = f"{ifttt_url}/{ifttt_event}/with/key/{ifttt_id}"
ifttt_params = {
    "url": ifttt_wh_url,
    "message": default_message,
    }

# mypy does not like this
new['webhooks'] = [ifttt_params]  # type: ignore[assignment]  # noqa: F821

with (p / 'config.json').open(mode='w') as f:
    json.dump(new, f, indent=4)

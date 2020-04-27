# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.2.1] - 2020-04-26
### Changed
- Branch `cloudflare` is merged with `master`. This is to simplify the code base, as the resulting features were not as divergent as previously thought.
- Because *IFTTT* is now mandatory to match branch `master`, the logger level for errors loading [ifttt.py](ifttt.py) is now `error`, not `warn`.
- Likewise, the error levels associated with *Cloudflare* are now `warn`, not `error`, in [config.py](config.py). In [main.py](main.py), *Cloudflare* functionality is enabled only if `config.CF_ENABLED` is `True`.
- Versioning since [1.2.0](#120---2020-04-26) now omits the `-cf` to reflect the merged branches.

## [1.2.0] - 2020-04-26
### Changed
- Project name is now "I've moved", as "public_ipaddr_check" is wordy and not fully accurate to its purpose (at a minimum, checks *and* alerts).
- `config.InvalidConfigError` now subclasses `RuntimeError` instead of an extraneous custom exception.
- `process.py` was renamed [main.py](main.py).
- The code that existed under `if __name__ == 'main':` now exists in its own function.
- `ipaddr.APIResponseError` now subclasses `ValueError`, in the same vein as `config.InvalidConfigError`.
- Assigned some hardcoded strings as variables instead, in case they ever need changing.
- Updated license years.
- In [config.yaml](config.yaml.example), subdomains are now nested directly under `'subdomains'` instead of elements of a list/array.
- You can now retrieve IDs of new subdomains in *Cloudflare* by calling `python cloudflare.py` and either supplying a list of subdomains separated by spaces or one time interactively. The resulting ID will be saved into [config.yaml](config.yaml.example).

## [1.1.3-cf] - 2019-12-25
### Changed
- Use `RotatingFileHandler` for logs
- Very minor changes to readme and syntactic changes to code

## [1.1.2-cf] - 2019-11-08
### Fixed
- Fixed issue when *ipify* returns an application error. Added an error to raise.

## [1.1.1-cf] - 2019-11-07
### Fixed
- Fixed missing argument in [`cloudflare.py`](cloudflare.py) `update_subdomain`
- Fixed `config['domain']` -> `config.DOMAIN`
- Added missing `requests` import to [`ifttt.py`](ifttt.py)
- On changing *Cloudflare* DNS records, changed the `data=` parameter to `json=`. Would not work with `data=`.

## [1.1.0-cf] - 2019-10-22
### Added
- *Cloudflare* update via API

### Changed
- `StreamHandler` is set to `INFO`, to output messages to `stdout`/`stderr`

### Fixed
- Blank/invalid IP addresses should no longer be ignored

## [1.0.1] - 2019-10-19
### Added
- logging; accessed in [`config.py`](config.py)

### Changed
- Broke up main [`process.py`](process.py) into:
    - [`config.py`](config.py): configuration handler
    - [`ifttt.py`](ifttt.py): IFTTT handler
    - [`ipaddr.py`](ipaddr.py): IP address retriever
- Instead of `sys.exit(1)`, `config.InvalidConfigError` is raised

## [1.0.0] - 2019-10-06
### Added
- Initial version

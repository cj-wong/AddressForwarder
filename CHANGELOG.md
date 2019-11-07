# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.1.1-cf] - 2019-11-07
### Fixed
- Fixed missing argument in [`cloudflare.py`](cloudflare.py) `update_subdomain`

## [1.1-cf] - 2019-10-22
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

## [1.0] - 2019-10-06
### Added
- Initial version

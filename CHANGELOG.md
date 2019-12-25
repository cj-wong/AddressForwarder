# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.4] - 2019-12-25
### Changed
- Use `RotatingFileHandler` for logs
- Very minor changes to readme and syntactic changes to code

## [1.0.3] - 2019-11-08
### Fixed
- Fixed issue when *ipify* returns an application error. Added an error to raise.

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

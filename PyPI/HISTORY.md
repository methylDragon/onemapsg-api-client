# OneMap API Client Changelog

## v1.0.2 - 2020_02_10

### Fixed

- Fix missing `mode` parameter in `get_public_transport_route()` call



## v1.0.1 - 2020_02_10

### Changed

- Allow functions that use onemap API tokens internally to continue running when token expiry is detected and token renewal occurs, instead of returning immediately

### Fixed

- Fix string formatting bug in `get_route()` and `get_public_transport_route()`



## v1.0.0 - 2019_07_09

### Added

- Initial release:
  - OneMapClient with full API
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
## [Unreleased](https://github.com/addicteduser/dnd-hp-calc-discordbot/compare/LATEST_TAG...HEAD) - YYYY-MM-DD

### Added
- for new features.

### Changed
- for changes in existing functionality.

### Deprecated
- for soon-to-be removed features.

### Removed
- for now removed features.

### Fixed
- for any bug fixes.

### Security
- in case of vulnerabilities.

-->

## [Unreleased](https://github.com/addicteduser/dnd-hp-calc-discordbot/compare/1.6.1...HEAD) - YYYY-MM-DD

## [1.6.1](https://github.com/addicteduser/dnd-hp-calc-discordbot/compare/1.6.0...1.6.1) - 2021-10-27

### Added

- Add `test-requirements.txt` for listing unit test dependencies.
- Add unit tests on parsing user input.

### Changed

- Migrate CI from Travis CI to GitHub Actions.

### Removed

- Remove usage of privileged server members intent (see [this](https://discordpy.readthedocs.io/en/stable/intents.html) for more info).

### Fixed

- Fix linking to Ko-Fi and GCash.

### Security

- Removed some hardcoded info.

## [1.6.0](https://github.com/addicteduser/dnd-hp-calc-discordbot/compare/1.5.1...1.6.0) - 2021-03-10

### Added

- Add `CHANGELOG.md`.
- Add `.env.sample`.
- Add `.travis.yml` for continuous integration.

### Changed

- Implement pylint suggestions.
- Move utility/helper modules to `utils/` and refactor affected code.
- Move unit tests to `tests/`.
- Accessing Discord token is now in `.env` instead of `secrets.py`.
- Optimize and parametrize ([`@pytest.mark.parametrize`](https://docs.pytest.org/en/stable/parametrize.html)) test functions.
- Add Travis CI badge in `README.md`.
- Include Ko-Fi and GCash links in Donation/Support section of `README.md`.

## [1.5.1](https://github.com/addicteduser/dnd-hp-calc-discordbot/compare/1.5.0...1.5.1) - 2021-02-08

### Added

- Add a link to GCash QR code in `?links`.

## [1.5.0](https://github.com/addicteduser/dnd-hp-calc-discordbot/compare/1.4.0...1.5.0) - 2021-02-05

### Added

- Add unit test.

### Changed

- Internal code restructuring and optimizations.
- Update discord.py from 1.3.4 to 1.6.0.

## [1.4.0](https://github.com/addicteduser/dnd-hp-calc-discordbot/compare/1.3.1...1.4.0) - 2020-09-09

### Changed

- Internal code restructuring.
- Lessen "Valron is typing..." time.
- Include `pal` to the list of `paladin` shortcuts.
- Remove `pally` from the list of `paladin` shortcuts.

## [1.3.1](https://github.com/addicteduser/dnd-hp-calc-discordbot/compare/1.3.0...1.3.1) - 2020-08-31

### Added

- Add activity status.

### Changed

- Lessened "Valron is typing..." time.

## [1.3.0](https://github.com/addicteduser/dnd-hp-calc-discordbot/compare/1.2.0...1.3.0) - 2020-08-28

### Added

- Add support for `artificer` class.
- Implement embeds.
- Add `?options` and `?links` commands.
- Implement "Valron is typing..." :3

### Changed

- Update help command from `?hphelp` to `?help`.
- Update list of classes (and shortcuts, e.g. `cleric` can be `cl` or `c`).
- Internal code restructuring and optimizations.

## [1.2.0](https://github.com/addicteduser/dnd-hp-calc-discordbot/compare/1.1.0...1.2.0) - 2020-07-22

### Changed

- Update discord.py from 1.2.5 to 1.3.4.

## [1.1.0](https://github.com/addicteduser/dnd-hp-calc-discordbot/compare/1.1.0...master) - 2020-03-25

### Changed

- Change the command usage from `!hp` to `?hp`.

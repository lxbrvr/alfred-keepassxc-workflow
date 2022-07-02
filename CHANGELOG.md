# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added 

- Clipboard timeout.
- Show note details in full text with `Opt ⌥ + Return ↵`.
- Request to check for workflow updates.

## [2.1.0] - 2022-04-10

### Added

- KeepassXC 2.7 support.
- Link to search instruction to README.md.
- Check KeepassXC CLI before executing commands.
- TOTP request for KeepassXC entries.

### Changed

- Requirements for KeepassXC version in README.md.

### Removed

- Support for KeepassXC versions before 2.7.

## [2.0.0] - 2022-03-24

### Added

- Python 3 support.
- Allow python interpreter selection in the settings.
- Check python interpreter before executing python commands.
- Don't reset alfred keyword and python path after resetting during express initialization.

### Changed

- Styling of README.md
- Simplify the usage section in README.md

### Removed

- Python 2 support.

## [1.2.0] - 2022-01-15

### Added

- Automatically paste entry attributes to front most app with `Command ⌘ + Return ↵`.

### Changed

- Log error to stderr after fail result of security and keepassxc-cli tools.
- Allow choosing a KeepassXC database with any file extension.

## [1.1.0] - 2021-09-25

### Added 

- Add the ability to manually remove the master password from a keychain.
- Add automatic removal of the master password from a keychain 
  after using "reset" and "init" commands.
- Show an error message when trying to configure a master password 
  without configured a keychain service or keychain account. 
- Remove an existing keychain record if the keychain name or the keychain 
  service name has been changed in the settings.

### Changed

- Change the names of the settings to be more informative
- Improve informativeness in dialog boxes.

## [1.0.0] - 2021-08-16

### Added

- First release

[2.1.0]: https://github.com/lxbrvr/alfred-keepassxc-workflow/compare/2.0.0...2.1.0
[2.0.0]: https://github.com/lxbrvr/alfred-keepassxc-workflow/compare/1.2.0...2.0.0
[1.2.0]: https://github.com/lxbrvr/alfred-keepassxc-workflow/compare/1.1.0...1.2.0
[1.1.0]: https://github.com/lxbrvr/alfred-keepassxc-workflow/compare/1.0.0...1.1.0
[1.0.0]: https://github.com/lxbrvr/alfred-keepassxc-workflow/releases/tag/1.0.0
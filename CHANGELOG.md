# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- automatically paste entry attributes to front most app with `Command ⌘ + Return ↵`.

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

[1.1.0]: https://github.com/lxbrvr/alfred-keepassxc-workflow/compare/1.0.0...1.1.0
[1.0.0]: https://github.com/lxbrvr/alfred-keepassxc-workflow/releases/tag/1.0.0
<div align="center">
  <h2>KeepassXC Alfred</h2>
  
  <p>
    <img alt="Logo" src="src/icon.png" width=200>
  </p>
  
  <p>Alfred workflow for fetching KeepassXC entries and coping their attributes.</p>

  <p>
    <a href="https://github.com/lxbrvr/alfred-keepassxc-workflow/releases/download/2.1.0/keepassxc-2.1.0.alfredworkflow">Download the latest version (2.1.0)</a>
  </p>
</div>

---

## Table of contents

- [Demo](#demo)
- [Features](#features)
- [Installation](#installation)
  * [Requirements](#requirements)
  * [Download and import](#download-and-import)
- [Usage](#usage)
  * [Initialization](#initialization)
  * [Commands](#commands)
  * [Alternative actions for attributes](#alternative-actions-for-attributes)
- [Development](#development)
  * [The first initialization](#the-first-initialization)
  * [Testing](#testing)
  * [Prepare info.plist](#prepare-infoplist)
  * [Build](#build)
  * [Other commands](#other-commands)

---

## Demo

![](demo.gif)

## Features

- Search KeepassXC entries.
- Copy different entry attributes. It includes title, username, password, url, notes.
- Request TOTP for KeepassXC entries.
- Comfortable configuration using Alfred's UI and MacOS modal windows
- There are different settings for displaying KeepassXC data in Alfred.
  For example, you can show KeepassXC attributes which you want.
  Or you can hide values displaying for KeepassXC attributes etc. 
  You can know more about it below.
- It works with KeepassXC key files
- It saves your KeepassXC master password to OSX Keychain.
- No dependencies. Only Alfred and KeepassXC.
- Automatically paste entry attributes to front most app with.
- Open urls in default browser.
- Clipboard timeout.

## Installation

#### Requirements

- Alfred 4+
- KeepassXC 2.7+
- Python 3.6+ 

#### Download and import

1. Download the latest version from [the releases page](https://github.com/lxbrvr/alfred-keepassxc-workflow/releases).
2. Import the downloaded file to Alfred.

## Usage

#### Initialization

Enter the command `kp:init`.

Before you can start to searching for KeepassXC entries you need to go through initialization.
It'll ask you about KeepassXC database, KeepassXC key file and KeepassXC master password.

#### Commands

| Command       | Description                                                                                                                                                                                                                                    |
|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `kp:init`     | Express initialization.                                                                                                                                                                                                                        |
| `kp <term>`   | Finds entries in a KeepassXC database based on `<term>` and shows them. The search behavior is the same as in the KeepassXC UI. For more information, see [here](https://keepassxc.org/docs/KeePassXC_UserGuide.html#_searching_the_database). |
| `kp:settings` | Settings for the workflow.                                                                                                                                                                                                                     |
| `kp:reset`    | Resets the workflow settings to default values. It also removes the master password from Keychain.                                                                                                                                             |
| `kp:about`    | Opens the workflow homepage in your default browser.                                                                                                                                                                                           |
| `kp:updates`  | Check for updates for the workflow.                                                                                                                                                                                                            |

#### Alternative actions for attributes

| Attribute name | Alternative action     | Description                                            |
|----------------|------------------------|--------------------------------------------------------|
| All            | `Command ⌘ + Return ↵` | Automatically paste entry attributes to front most app |
| Notes          | `Opt ⌥ + Return ↵`     | Show note details in full text                         | 
| Url            | `Opt ⌥ + Return ↵`     | Open url in a default browser                          | 

## Development

#### The first initialization

Run `make install`.

It creates a symlink in the alfred workflows directory to `src` directory.

#### Testing

1. Install virtualenv using system python (`/usr/bin/python3`)
2. Enter to virtualenv
3. Install requirements using `pip install -r requirements.txt`
4. Run `make test`/`make vtest` from project root directory

#### Prepare info.plist

Run `make prepare_plist version=<VERSION>` where `<VERSION>` is a new workflow version.

This command prepares the info.plist for a build: sets default values, sets title etc.

Note this command removes all environment variables not allowed for export from info.plist.

#### Build

Run `make build version=<VERSION>` where `<VERSION>` is a new workflow version.

Build is an operation that creates `.alredworkflow` file. 

`.alfredworkflow` file is a zip file so `build` command archives the source code directory
and changes the file extension from zip to alfredworkflow.

### Other commands

Run `make help` to see other commands and their description.
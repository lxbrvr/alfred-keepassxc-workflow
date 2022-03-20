<div align="center">
  <h2>KeepassXC Alfred</h2>
  
  <p>
    <img alt="Logo" src="src/icon.png" width=200>
  </p>
  
  <p>Alfred workflow for fetching KeepassXC entries and coping their attributes.</p>

  <p>
    <a href="https://github.com/lxbrvr/alfred-keepassxc-workflow/releases/download/1.2.0/keepassxc-1.2.0.alfredworkflow">Download the latest version (1.2.0)</a>
  </p>
</div>

---

## Table of contents

- [Demo](#demo)
- [Features](#features)
- [Installation](#installation)
  * [Requirements](#requirements)
  * [Download and import](#download-and-import)
- [Using](#using)
  * [Initialization](#initialization)
  * [Search KeepassXC entries](#search-keepassxc-entries)
  * [Reset settings](#reset-settings)
  * [Settings](#settings)
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

- Search KeepassXC entries
- Copy different entry attributes. It includes title, username, password, url, notes
- Comfortable configuration using Alfred's UI and MacOS modal windows
- There are different settings for displaying KeepassXC data in Alfred.
  For example, you can show KeepassXC attributes which you want.
  Or you can hide values displaying for KeepassXC attributes etc. 
  You can know more about it below.
- It works with KeepassXC key files
- It saves your KeepassXC master password to OSX Keychain.
- No dependencies. Only Alfred and KeepassXC.
- Automatically paste entry attributes to front most app with `Command ⌘ + Return ↵`.

## Installation

### Requirements

- Alfred 4+
- KeepassXC
- Monterey 12.3+ 

### Download and import

1. Download the latest version from [the releases page](https://github.com/lxbrvr/alfred-keepassxc-workflow/releases).
2. Import the downloaded file to Alfred.

## Using

### Initialization

There are three ways to configure the workflow.

**The first and fastest way**:

Call Alfred, type `kp` or type `kp:init` and select "Express initialization".
It'll ask you about KeepassXC database, KeepassXC key file and KeepassXC master password.

**The second way**:

Call Alfred, type `kp` or type `kp:settings` and select "Settings".
There are all parameters of the workflow. Just change them to desired.
The settings described [below](#Settings).

**The third way (not recommended)**:

1. Open the workflow in Alfred 
2. Click on "Configure workflow and variables".
3. Change values of environment variables in "Workflow Environment Variables".
4. Click "Save" button.

That's it. Now you can search your KeepassXC entries using Alfred.

### Search KeepassXC entries

1. Call Alfred and type `kp <desired KeepassXC entry name>`. It'll show found entries. 
2. Select some entry. It'll show entry attribute names. For example title, username, password etc.
3. Select the attribute name. An attribute value will be copied to clipboard.

### Reset settings

Call Alfred and type `kp` or `kp:reset`. It'll ask you for confirmation. 
If you select `yes` then workflow will be reset to default settings and will
delete a password from Keychain.

### Settings

| Title in Alfred                         | Environment variable      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|-----------------------------------------|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Keyword name for name Alfred's workflow | alfred_keyword            | Keyword name for calling of Alfred's workflow. Default value is `kp`.                                                                                                                                                                                                                                                                                                                                                                       |
| KeepassXC database                      | keepassxc_db_path         | KeepassXC database file on system. It requires `.kdbx` file.                                                                                                                                                                                                                                                                                                                                                                                |
| KeepassXC master password               | keepassxc_master_password | The master password for a KeepassXC database. If a password does not exist then it will be added to keychain. If a password already exists then the workflow will ask you what you want to do with it. You can remove it from your keychain or change it to another one. If your KeepassXC database does not have a password then just leave the password field blank. Note that the master password is not saved in environment variables. |
| KeepassXC key file                      | keepassxc_keyfile_path    | KeepassXC key file on system. This parameter is optional.                                                                                                                                                                                                                                                                                                                                                                                   |
| Keychain account                        | keychain_account          | A name of keychain account. By default it's the name of your system user.                                                                                                                                                                                                                                                                                                                                                                   |
| Keychain service                        | keychain_service          | A name of keychain service. By default it's `com.lxbrvr.keepassxcalfred`                                                                                                                                                                                                                                                                                                                                                                    |
| Show attribute values in Alfred         | show_attribute_values     | By default you can see KeepassXC attribute values in Alfred. You can hide these values and only show attribute names.                                                                                                                                                                                                                                                                                                                       |
| Show unfilled attributes in Alfred      | show_unfilled_attributes  | By default you can see KeepassXC entries attributes which have some data. You can disable it. For example if the attribute `username` has no any value then it won't display this one.                                                                                                                                                                                                                                                      |
| Desired attributes to show in Alfred    | desired_attributes        | By default it only shows title, username, password, url, notes. You can change this list.                                                                                                                                                                                                                                                                                                                                                   |
| Show passwords in Alfred                | show_passwords            | By default there are no real passwords displayed for KeepassXC entries. If you want to see them then enable it.                                                                                                                                                                                                                                                                                                                             |
| KeepassXC entries delimiter             | entry_delimiter           | If KeepassXC entries are in some folders then it'll show something like this: `folder › nested folder › entry`. You can change the symbol ` › ` to desired.                                                                                                                                                                                                                                                                                 |
| KeepassXC CLI path                      | keepassxc_cli_path        | Path to KeepassXC CLI tool. By default the path is `/usr/local/bin/keepassxc-cli`.                                                                                                                                                                                                                                                                                                                                                          |

## Development

### The first initialization

Run `make install`.

It creates a symlink in the alfred workflows directory to `src` directory.

### Testing

1. Install virtualenv using system python (`/usr/bin/python2`)
2. Enter to virtualenv
3. Install requirements using `pip install -r requirements.txt`
4. Run `make test`/`make vtest` from project root directory

### Prepare info.plist

Run `make prepare_plist version=<VERSION>` where `<VERSION>` is a new workflow version.

This command prepares the info.plist for a build: sets default values, sets title etc.

Note this command removes all environment variables not allowed for export from info.plist.

### Build

Run `make build version=<VERSION>` where `<VERSION>` is a new workflow version.

Build is an operation that creates `.alredworkflow` file. 

`.alfredworkflow` file is a zip file so `build` command archives the source code directory
and changes the file extension from zip to alfredworkflow.

### Other commands

Run `make help` to see other commands and their description.
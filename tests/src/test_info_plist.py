def test_not_allowed_to_export_envs(info_plist):
    actual_variables = info_plist["variablesdontexport"]
    expected_variables = [
        "keepassxc_db_path",
        "keepassxc_cli_path",
        "keychain_account",
        "desired_attributes",
        "keepassxc_keyfile_path",
        "keepassxc_master_password",
        "keychain_service",
        "show_attribute_values",
        "show_unfilled_attributes",
        "entry_delimiter",
        "show_passwords",
        "python_path",
    ]

    assert actual_variables.sort() == expected_variables.sort()


def test_variables_content(info_plist):
    actual_content = info_plist["variables"]
    non_empty_variables = ["alfred_keyword", "python_path"]
    empty_variables = [
        "keepassxc_db_path",
        "keepassxc_cli_path",
        "keychain_account",
        "desired_attributes",
        "keepassxc_keyfile_path",
        "keepassxc_master_password",
        "keychain_service",
        "show_attribute_values",
        "show_unfilled_attributes",
        "entry_delimiter",
        "show_passwords",
        "show_totp_request",
    ]

    all_variables = non_empty_variables + empty_variables

    assert actual_content["alfred_keyword"] == "kp"
    assert actual_content["python_path"] == "/usr/bin/python3"
    assert set(actual_content.keys()) == set(all_variables)
    assert all(actual_content[i] == "" for i in empty_variables)


def test_web_address(info_plist):
    actual_address = info_plist["webaddress"]
    expected_address = "https://github.com/lxbrvr/alfred-keepassxc-workflow"

    assert actual_address == expected_address


def test_description(info_plist):
    actual_description = info_plist["description"]
    expected_description = "Alfred workflow for fetching KeepassXC entries and coping their attributes."

    assert actual_description == expected_description


def test_bundle_id(info_plist):
    actual_bundle_id = info_plist["bundleid"]
    expected_bundle_id = "com.lxbrvr.keepassxcalfred"

    assert actual_bundle_id == expected_bundle_id


def test_created_by(info_plist):
    actual_created_by = info_plist["createdby"]
    expected_created_by = "Alexander Abrosimov"

    assert actual_created_by == expected_created_by


def test_name(info_plist):
    actual_name = info_plist["name"]
    expected_name = "KeepassXC Alfred"

    assert actual_name == expected_name


def test_readme(info_plist):
    actual_readme = info_plist["readme"]
    expected_readme = ""

    assert actual_readme == expected_readme

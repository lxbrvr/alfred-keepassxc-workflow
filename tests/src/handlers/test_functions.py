import argparse
from collections import namedtuple

import pytest

from handlers import (
    fetch_handler,
    list_settings_handler,
    require_password,
    search_handler,
    validate_settings,
)
from helpers import cast_bool_to_yesno


class TestValidateSettingsDecorator:
    def test_with_invalid_settings(self, mocker, invalid_settings):
        mocker.patch("handlers.settings", new=invalid_settings)
        add_item_mock = mocker.patch("handlers.AlfredScriptFilter.add_item")
        send_mock = mocker.patch("handlers.AlfredScriptFilter.send")
        handler_mock = mocker.Mock()
        validate_settings(handler_mock)()

        send_mock.assert_called_once()
        handler_mock.assert_not_called()

        add_item_mock.assert_any_call(
            title="Configure your settings",
            subtitle="Press to go to settings.",
            arg="settings",
        )

        add_item_mock.assert_any_call(
            title="Express initialization", subtitle="Press to go to express initialization", arg="express"
        )

        assert add_item_mock.call_count == 2

    def test_with_valid_settings(self, mocker, valid_settings):
        mocker.patch("handlers.settings", new=valid_settings)
        handler_mock = mocker.Mock()
        validate_settings(handler_mock)()

        handler_mock.assert_called_once()


class TestRequirePasswordDecorator:
    def test_without_password_in_settings(self, mocker, configurable_valid_settings):
        configurable_valid_settings(keepassxc_master_password="")
        add_item_mock = mocker.patch("handlers.AlfredScriptFilter.add_item")
        handler_mock = mocker.Mock()
        send_mock = mocker.patch("handlers.AlfredScriptFilter.send")
        require_password(handler_mock)()

        send_mock.assert_called_once()
        handler_mock.assert_not_called()

        add_item_mock.assert_called_once_with(
            title="Please enter your password",
            subtitle="Press to open a dialog window",
            arg="keepassxc_master_password",
        )

    def test_with_password_in_settings(self, mocker, configurable_valid_settings):
        configurable_valid_settings(keepassxc_master_password="password")
        handler_mock = mocker.Mock()
        send_mock = mocker.patch("handlers.AlfredScriptFilter.send")
        require_password(handler_mock)()

        send_mock.assert_not_called()
        handler_mock.assert_called_once()


class TestSearchHandler:
    def test_kp_client_error(self, mocker, valid_settings, keepassxc_client):
        mocker.patch.object(keepassxc_client, "search", side_effect=OSError)
        mocker.patch("handlers.initialize_keepassxc_client", return_value=keepassxc_client)
        add_item_mock = mocker.patch("handlers.AlfredScriptFilter.add_item")
        send_mock = mocker.patch("handlers.AlfredScriptFilter.send")
        parsed_args = namedtuple("parsed_args", "query")

        with pytest.raises(OSError):
            search_handler(parsed_args)

        add_item_mock.assert_called_with(
            title="There aren't matches or something went wrong.",
            is_valid=False,
        )
        send_mock.assert_called_once()

    @pytest.mark.parametrize(
        "kp_output, expected_title, expected_arg",
        [
            ("/dir1/dir2/entry", "dir1{delimiter}dir2{delimiter}entry", "/dir1/dir2/entry"),
            ("/entry", "entry", "/entry"),
            ("/dir1/entry", "dir1{delimiter}entry", "/dir1/entry"),
        ],
    )
    def test_success_output(
        self, mocker, environ_factory, valid_settings, keepassxc_client, kp_output, expected_title, expected_arg
    ):
        environ_factory(entry_delimiter=" > ")
        mocker.patch.object(keepassxc_client, "search", return_value=[kp_output])
        mocker.patch("handlers.initialize_keepassxc_client", return_value=keepassxc_client)
        add_item_mock = mocker.patch("handlers.AlfredScriptFilter.add_item")
        send_mock = mocker.patch("handlers.AlfredScriptFilter.send")
        add_variable_mock = mocker.patch("handlers.AlfredScriptFilter.add_variable")
        parsed_args = namedtuple("parsed_args", "query")
        search_handler(parsed_args)

        add_item_mock.assert_called_with(
            title=expected_title.format(delimiter=valid_settings.ENTRY_DELIMITER.value), arg=expected_arg
        )
        send_mock.assert_called_once()
        add_variable_mock.assert_called_with("USER_QUERY", parsed_args.query)


class TestFetchHandler:
    @pytest.mark.parametrize(
        "desired_attributes, expected_added_item_titles",
        [
            ("title", ["Title"]),
            ("title,username", ["Title", "Username"]),
            ("title,username,password", ["Title", "Username", "Password"]),
            ("title,username,password,url", ["Title", "Username", "Password", "Url"]),
            ("title,username,password,url,notes", ["Title", "Username", "Password", "Url", "Notes"]),
        ],
    )
    def test_desired_attributes(
        self,
        mocker,
        valid_settings,
        expected_added_item_titles,
        keepassxc_client,
        environ_factory,
        desired_attributes,
        keepassxc_item,
    ):
        environ_factory(
            desired_attributes=desired_attributes,
            show_attribute_values="yes",
            show_passwords="yes",
        )

        mocker.patch.object(keepassxc_client, "show", return_value=keepassxc_item)
        mocker.patch("handlers.initialize_keepassxc_client", return_value=keepassxc_client)
        add_item_mock = mocker.patch("handlers.AlfredScriptFilter.add_item")
        send_mock = mocker.patch("handlers.AlfredScriptFilter.send")
        parsed_args = namedtuple("parsed_args", "query")
        fetch_handler(parsed_args)

        send_mock.assert_called_once()

        for expected_title in expected_added_item_titles:
            add_item_mock.assert_any_call(
                title=expected_title,
                is_valid=True,
                subtitle=getattr(keepassxc_item, expected_title.lower()),
                arg=expected_title.lower(),
                mods=mocker.ANY,
            )

        add_item_mock.assert_any_call(title="← Back", subtitle="Back to search", arg="back")
        assert add_item_mock.call_count == len(expected_added_item_titles) + 1  # 1 is back button

    @pytest.mark.parametrize(
        "show_unfilled_attributes, empty_attributes, expected_add_items",
        [
            (
                "no",
                [],
                [
                    {"title": "Title", "subtitle": "value", "is_valid": True, "arg": "value"},
                    {"title": "Username", "subtitle": "value", "is_valid": True, "arg": "value"},
                    {"title": "Password", "subtitle": "value", "is_valid": True, "arg": "value"},
                    {"title": "Url", "subtitle": "value", "is_valid": True, "arg": "value"},
                    {"title": "Notes", "subtitle": "value", "is_valid": True, "arg": "value"},
                ],
            ),
            (
                "no",
                ["title"],
                [
                    {"title": "Username", "subtitle": "value", "is_valid": True, "arg": "value"},
                    {"title": "Password", "subtitle": "value", "is_valid": True, "arg": "value"},
                    {"title": "Url", "subtitle": "value", "is_valid": True, "arg": "value"},
                    {"title": "Notes", "subtitle": "value", "is_valid": True, "arg": "value"},
                ],
            ),
            (
                "no",
                ["title", "username"],
                [
                    {"title": "Password", "subtitle": "value", "is_valid": True, "arg": "value"},
                    {"title": "Url", "subtitle": "value", "is_valid": True, "arg": "value"},
                    {"title": "Notes", "subtitle": "value", "is_valid": True, "arg": "value"},
                ],
            ),
            (
                "no",
                ["title", "username", "password"],
                [
                    {"title": "Url", "subtitle": "value", "is_valid": True, "arg": "value"},
                    {"title": "Notes", "subtitle": "value", "is_valid": True, "arg": "value"},
                ],
            ),
            (
                "no",
                ["title", "username", "password", "url"],
                [
                    {"title": "Notes", "subtitle": "value", "is_valid": True, "arg": "value"},
                ],
            ),
            ("no", ["title", "username", "password", "url", "notes"], []),
            (
                "yes",
                [],
                [
                    {"title": "Title", "subtitle": "value", "is_valid": True, "arg": "value"},
                    {"title": "Username", "subtitle": "value", "is_valid": True, "arg": "value"},
                    {"title": "Password", "subtitle": "value", "is_valid": True, "arg": "value"},
                    {"title": "Url", "subtitle": "value", "is_valid": True, "arg": "value"},
                    {"title": "Notes", "subtitle": "value", "is_valid": True, "arg": "value"},
                ],
            ),
            (
                "yes",
                ["title"],
                [
                    {"title": "Title (empty)", "subtitle": None, "is_valid": False, "arg": None},
                    {"title": "Username", "subtitle": "value", "is_valid": True, "arg": "value"},
                    {"title": "Password", "subtitle": "value", "is_valid": True, "arg": "value"},
                    {"title": "Url", "subtitle": "value", "is_valid": True, "arg": "value"},
                    {"title": "Notes", "subtitle": "value", "is_valid": True, "arg": "value"},
                ],
            ),
            (
                "yes",
                ["title", "username"],
                [
                    {"title": "Title (empty)", "subtitle": None, "is_valid": False, "arg": None},
                    {"title": "Username (empty)", "subtitle": None, "is_valid": False, "arg": None},
                    {"title": "Password", "subtitle": "value", "is_valid": True, "arg": "value"},
                    {"title": "Url", "subtitle": "value", "is_valid": True, "arg": "value"},
                    {"title": "Notes", "subtitle": "value", "is_valid": True, "arg": "value"},
                ],
            ),
            (
                "yes",
                ["title", "username", "password"],
                [
                    {"title": "Title (empty)", "subtitle": None, "is_valid": False, "arg": None},
                    {"title": "Username (empty)", "subtitle": None, "is_valid": False, "arg": None},
                    {"title": "Password (empty)", "subtitle": None, "is_valid": False, "arg": None},
                    {"title": "Url", "subtitle": "value", "is_valid": True, "arg": "value"},
                    {"title": "Notes", "subtitle": "value", "is_valid": True, "arg": "value"},
                ],
            ),
            (
                "yes",
                ["title", "username", "password", "url"],
                [
                    {"title": "Title (empty)", "subtitle": None, "is_valid": False, "arg": None},
                    {"title": "Username (empty)", "subtitle": None, "is_valid": False, "arg": None},
                    {"title": "Password (empty)", "subtitle": None, "is_valid": False, "arg": None},
                    {"title": "Url (empty)", "subtitle": None, "is_valid": False, "arg": None},
                    {"title": "Notes", "subtitle": "value", "is_valid": True, "arg": "value"},
                ],
            ),
            (
                "yes",
                ["title", "username", "password", "url", "notes"],
                [
                    {"title": "Title (empty)", "subtitle": None, "is_valid": False, "arg": None},
                    {"title": "Username (empty)", "subtitle": None, "is_valid": False, "arg": None},
                    {"title": "Password (empty)", "subtitle": None, "is_valid": False, "arg": None},
                    {"title": "Url (empty)", "subtitle": None, "is_valid": False, "arg": None},
                    {"title": "Notes (empty)", "subtitle": None, "is_valid": False, "arg": None},
                ],
            ),
        ],
    )
    def test_show_unfilled_attributes(
        self,
        mocker,
        valid_settings,
        environ_factory,
        keepassxc_client,
        keepassxc_item,
        show_unfilled_attributes,
        empty_attributes,
        expected_add_items,
    ):
        environ_factory(
            desired_attributes="title,username,password,url,notes",
            show_attribute_values="yes",
            show_passwords="yes",
            show_unfilled_attributes=show_unfilled_attributes,
        )

        keepassxc_item_values = "value"

        for empty_attribute in ["title", "username", "password", "url", "notes"]:
            setattr(keepassxc_item, empty_attribute, keepassxc_item_values)

        for empty_attribute in empty_attributes:
            setattr(keepassxc_item, empty_attribute, None)

        mocker.patch.object(keepassxc_client, "show", return_value=keepassxc_item)
        mocker.patch("handlers.initialize_keepassxc_client", return_value=keepassxc_client)
        add_item_mock = mocker.patch("handlers.AlfredScriptFilter.add_item")
        send_mock = mocker.patch("handlers.AlfredScriptFilter.send")
        parsed_args = namedtuple("parsed_args", "query")
        fetch_handler(parsed_args)

        send_mock.assert_called_once()
        add_item_mock.assert_any_call(title="← Back", subtitle="Back to search", arg="back")
        assert add_item_mock.call_count == len(expected_add_items) + 1  # 1 is back button

        for expected_add_item in expected_add_items:
            expected_add_item["mods"] = mocker.ANY
            add_item_mock.assert_any_call(**expected_add_item)

    @pytest.mark.parametrize(
        "show_password, password, expected_add_item",
        [
            ("yes", "password", {"title": "Password", "subtitle": "password", "is_valid": True, "arg": "password"}),
            ("no", "password", {"title": "Password", "subtitle": "••••••••", "is_valid": True, "arg": "password"}),
        ],
    )
    def test_show_password(
        self,
        mocker,
        valid_settings,
        environ_factory,
        keepassxc_client,
        keepassxc_item,
        show_password,
        password,
        expected_add_item,
    ):
        environ_factory(
            desired_attributes="password",
            show_attribute_values="yes",
            show_passwords=show_password,
            show_unfilled_attributes="yes",
        )

        setattr(keepassxc_item, "password", password)

        mocker.patch.object(keepassxc_client, "show", return_value=keepassxc_item)
        mocker.patch("handlers.initialize_keepassxc_client", return_value=keepassxc_client)
        add_item_mock = mocker.patch("handlers.AlfredScriptFilter.add_item")
        send_mock = mocker.patch("handlers.AlfredScriptFilter.send")
        parsed_args = namedtuple("parsed_args", "query")
        expected_add_item["mods"] = mocker.ANY
        fetch_handler(parsed_args)

        send_mock.assert_called_once()
        add_item_mock.assert_any_call(title="← Back", subtitle="Back to search", arg="back")
        assert add_item_mock.call_count == 2  # 1 is back button
        add_item_mock.assert_any_call(**expected_add_item)

    @pytest.mark.parametrize("show_attribute_values, expected_subtitle", [("yes", "value"), ("no", None)])
    def test_show_attribute_value(
        self,
        mocker,
        valid_settings,
        environ_factory,
        keepassxc_client,
        keepassxc_item,
        expected_subtitle,
        show_attribute_values,
    ):
        environ_factory(
            desired_attributes="title,username,password,url,notes",
            show_attribute_values=show_attribute_values,
            show_passwords="yes",
            show_unfilled_attributes="yes",
        )

        keepassxc_item_values = "value"

        for empty_attribute in ["title", "username", "password", "url", "notes"]:
            setattr(keepassxc_item, empty_attribute, keepassxc_item_values)

        mocker.patch.object(keepassxc_client, "show", return_value=keepassxc_item)
        mocker.patch("handlers.initialize_keepassxc_client", return_value=keepassxc_client)
        alfred_mod = mocker.patch("handlers.AlfredMod")
        alfred_mod_instance = alfred_mod.return_value

        add_item_mock = mocker.patch("handlers.AlfredScriptFilter.add_item")
        send_mock = mocker.patch("handlers.AlfredScriptFilter.send")
        parsed_args = namedtuple("parsed_args", "query")
        fetch_handler(parsed_args)

        send_mock.assert_called_once()
        add_item_mock.assert_any_call(title="← Back", subtitle="Back to search", arg="back")
        assert add_item_mock.call_count == 6  # 1 is back button

        for attribute in ["title", "username", "password", "url", "notes"]:
            add_item_mock.assert_any_call(
                title=attribute.title(),
                subtitle=expected_subtitle,
                is_valid=True,
                arg=keepassxc_item_values,
                mods=[alfred_mod_instance],
            )

    def test_mod(self, valid_settings, environ_factory, keepassxc_item, keepassxc_client, mocker):
        environ_factory(desired_attributes="password", show_unfilled_attributes="yes")
        keepassxc_item.password = "password"
        mocker.patch.object(keepassxc_client, "show", return_value=keepassxc_item)
        mocker.patch("handlers.initialize_keepassxc_client", return_value=keepassxc_client)
        mocker.patch("handlers.AlfredScriptFilter.add_item")
        mocker.patch("handlers.AlfredScriptFilter.send")
        mod_mock = mocker.patch("handlers.AlfredMod")
        mod_instance_mock = mod_mock.return_value
        parsed_args = namedtuple("parsed_args", "query")
        fetch_handler(parsed_args)

        mod_mock.assert_called_once_with(
            action="cmd",
            subtitle="Copy and paste to front most app.",
            arg=keepassxc_item.password,
        )
        mod_instance_mock.add_variable.assert_called_once_with("USER_ACTION", "mod")


class TestListSettingsHandler:
    def test_added_items(self, mocker, valid_settings):
        add_item_mock = mocker.patch("handlers.AlfredScriptFilter.add_item")
        send_mock = mocker.patch("handlers.AlfredScriptFilter.send")
        list_settings_handler(argparse.Namespace())

        send_mock.assert_called_once()
        add_item_mock.assert_any_call(
            title="Keyword name for Alfred's workflow",
            subtitle=valid_settings.ALFRED_KEYWORD.raw_value,
            arg=valid_settings.ALFRED_KEYWORD.name,
        )

        add_item_mock.assert_any_call(
            title="KeepassXC database",
            subtitle=valid_settings.KEEPASSXC_DB_PATH.raw_value,
            arg=valid_settings.KEEPASSXC_DB_PATH.name,
        )

        add_item_mock.assert_any_call(
            title="KeepassXC master password",
            subtitle=valid_settings.KEEPASSXC_MASTER_PASSWORD.raw_value,
            arg=valid_settings.KEEPASSXC_MASTER_PASSWORD.name,
        )

        add_item_mock.assert_any_call(
            title="KeepassXC key file",
            subtitle=valid_settings.KEEPASSXC_KEYFILE_PATH.raw_value,
            arg=valid_settings.KEEPASSXC_KEYFILE_PATH.name,
        )

        add_item_mock.assert_any_call(
            title="Keychain account name",
            subtitle=valid_settings.KEYCHAIN_ACCOUNT.raw_value,
            arg=valid_settings.KEYCHAIN_ACCOUNT.name,
        )

        add_item_mock.assert_any_call(
            title="Keychain service name",
            subtitle=valid_settings.KEYCHAIN_SERVICE.raw_value,
            arg=valid_settings.KEYCHAIN_SERVICE.name,
        )

        add_item_mock.assert_any_call(
            title="Display attribute values of KeepassXC records",
            subtitle=cast_bool_to_yesno(valid_settings.SHOW_ATTRIBUTE_VALUES.value),
            arg=valid_settings.SHOW_ATTRIBUTE_VALUES.name,
        )

        add_item_mock.assert_any_call(
            title="Display blank attributes of KeepassXC records",
            subtitle=cast_bool_to_yesno(valid_settings.SHOW_UNFILLED_ATTRIBUTES.value),
            arg=valid_settings.SHOW_UNFILLED_ATTRIBUTES.name,
        )

        add_item_mock.assert_any_call(
            title="Attributes of KeepassXC records to display",
            subtitle=valid_settings.DESIRED_ATTRIBUTES.raw_value.replace(",", ", "),
            arg=valid_settings.DESIRED_ATTRIBUTES.name,
        )

        add_item_mock.assert_any_call(
            title="Display real passwords of KeepassXC records",
            subtitle=cast_bool_to_yesno(valid_settings.SHOW_PASSWORDS.value),
            arg=valid_settings.SHOW_PASSWORDS.name,
        )

        add_item_mock.assert_any_call(
            title="Delimiter in KeepassXC records list",
            subtitle=valid_settings.ENTRY_DELIMITER.raw_value,
            arg=valid_settings.ENTRY_DELIMITER.name,
        )

        add_item_mock.assert_any_call(
            title="KeepassXC CLI path",
            subtitle=valid_settings.KEEPASSXC_CLI_PATH.raw_value,
            arg=valid_settings.KEEPASSXC_CLI_PATH.name,
        )

        add_item_mock.assert_any_call(
            title="Python path",
            subtitle=valid_settings.PYTHON_PATH.raw_value,
            arg=valid_settings.PYTHON_PATH.name,
        )

        assert add_item_mock.call_count == 13

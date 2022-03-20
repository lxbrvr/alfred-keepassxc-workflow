import sys

import pytest

from alfred import AlfredMod, AlfredModActionEnum, AlfredScriptFilter


class TestInitMethod(object):
    def test_attributes_initialization(self):
        script_filter = AlfredScriptFilter()

        assert script_filter.items == []
        assert script_filter.variables == {}


class TestAddVariableMethod(object):
    def test_variables_updating(self, alfred_script_filter):
        incoming_key, incoming_value = 1, 1
        alfred_script_filter.add_variable(incoming_key, incoming_value)

        assert alfred_script_filter.variables.get(incoming_key) == incoming_value


class TestAddItemMethod(object):
    @pytest.mark.parametrize(
        "title, subtitle, is_valid, arg, mods, expected_item",
        [
            ("a", None, None, None, None, {"title": "a", "valid": True}),
            ("a", "b", None, None, None, {"title": "a", "subtitle": "b", "valid": True}),
            ("a", "b", False, None, None, {"title": "a", "subtitle": "b", "valid": False}),
            ("a", "b", False, "c", None, {"title": "a", "subtitle": "b", "valid": False, "arg": "c"}),
            ("a", "b", True, "c", None, {"title": "a", "subtitle": "b", "valid": True, "arg": "c"}),
            (
                "a",
                None,
                None,
                None,
                [AlfredMod(action=AlfredModActionEnum.CMD, subtitle="s", arg="arg", is_valid=True)],
                {
                    "title": "a",
                    "valid": True,
                    "mods": {"cmd": {"subtitle": "s", "valid": True, "arg": "arg", "variables": {}}},
                },
            ),
        ],
    )
    def test_different_incoming_parameters(
        self, alfred_script_filter, title, subtitle, is_valid, arg, mods, expected_item
    ):
        incoming_parameters = {"title": title}

        if subtitle:
            incoming_parameters["subtitle"] = subtitle

        if isinstance(is_valid, bool):
            incoming_parameters["is_valid"] = is_valid

        if arg:
            incoming_parameters["arg"] = arg

        if mods:
            incoming_parameters["mods"] = mods

        alfred_script_filter.add_item(**incoming_parameters)

        assert len(alfred_script_filter.items) == 1
        assert alfred_script_filter.items[0] == expected_item

    @pytest.mark.parametrize("number_of_items, expected_number_of_items", [(1, 1), (2, 2), (3, 3)])
    def test_appending_multiple_items(self, alfred_script_filter, number_of_items, expected_number_of_items):
        for _ in range(number_of_items):
            alfred_script_filter.add_item(title="title")

        assert len(alfred_script_filter.items) == expected_number_of_items

    @pytest.mark.parametrize("number_of_items, expected_number_of_items", [(1, 1), (2, 2), (3, 3)])
    def test_appending_of_multiple_mods(self, alfred_script_filter, number_of_items, expected_number_of_items, mocker):
        alfred_script_filter.add_item(
            title="title",
            subtitle="",
            is_valid=True,
            arg="arg",
            mods=[mocker.Mock() for _ in range(number_of_items)],
        )

        assert len(alfred_script_filter.items[0].get("mods", {})) == expected_number_of_items


class TestSendMethod(object):
    def test_with_only_items(self, alfred_script_filter, mocker):
        alfred_script_filter.add_item(title="title")
        dump_mock = mocker.patch("alfred.json.dump")
        stdout_mock = mocker.patch("alfred.sys.stdout")
        alfred_script_filter.send()

        expected_data = {"items": [{"title": "title"}]}

        assert dump_mock.called_with(expected_data, sys.stdout)
        stdout_mock.flush.assert_called_once()

    def test_with_items_and_variables(self, alfred_script_filter, mocker):
        alfred_script_filter.add_item(title="title")
        alfred_script_filter.add_variable("key", "value")
        dump_mock = mocker.patch("alfred.json.dump")
        stdout_mock = mocker.patch("alfred.sys.stdout")
        alfred_script_filter.send()

        expected_data = {
            "items": [{"title": "title", "mods": mocker.ANY}],
            "variables": {"key": "value"},
        }

        assert dump_mock.called_with(expected_data, sys.stdout)
        stdout_mock.flush.assert_called_once()

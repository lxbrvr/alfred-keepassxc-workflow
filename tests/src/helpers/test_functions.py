import pytest

from helpers import (
    cast_bool_to_yesno,
    cast_value_to_bool,
    split_string_with_commas,
)


class TestCastValueToBool(object):
    @pytest.mark.parametrize(
        "incoming_value, expected_boolean",
        [
            ("1", True),
            ("true", True),
            ("yes", True),
            (True, True),
            (1, False),
            (False, False),
            ("something", False),
        ],
    )
    def test(self, incoming_value, expected_boolean):
        actual_boolean = cast_value_to_bool(incoming_value)
        assert actual_boolean == expected_boolean


class TestSplitStringWithCommas(object):
    @pytest.mark.parametrize(
        "incoming_value, expected_list",
        [
            ("a,b,c", ["a", "b", "c"]),
            (" a, b ,  c ", ["a", "b", "c"]),
            ("abc", ["abc"]),
            ("", []),
        ],
    )
    def test(self, incoming_value, expected_list):
        actual_list = split_string_with_commas(incoming_value)
        assert actual_list == expected_list


class TestCastBoolToYesNo(object):
    @pytest.mark.parametrize("incoming_value, expected_string", [(True, "Yes"), (False, "No")])
    def test(self, incoming_value, expected_string):
        actual_string = cast_bool_to_yesno(incoming_value)
        assert actual_string == expected_string

import pytest as pytest

from alfred import AlfredMod


class TestInitMethod(object):
    @pytest.mark.parametrize(
        "action, subtitle, arg, is_valid",
        [
            ("action", "subtitle", "arg", True),
            ("action", "subtitle", "arg", False),
        ]
    )
    def test_initial_data(self, action, subtitle, arg, is_valid):
        mod = AlfredMod(action=action, is_valid=is_valid, subtitle=subtitle, arg=arg)

        assert mod.action == action
        assert mod.is_valid == is_valid
        assert mod.subtitle == subtitle
        assert mod.arg == arg
        assert mod.variables == {}


class TestAddVariableMethod(object):
    def test_variables_updating(self):
        incoming_key, incoming_value = 1, 1
        mod = AlfredMod("", "", "")
        mod.add_variable(incoming_key, incoming_value)

        assert mod.variables.get(incoming_key) == incoming_value

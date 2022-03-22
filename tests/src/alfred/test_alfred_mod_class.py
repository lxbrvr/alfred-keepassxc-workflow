import pytest as pytest

from alfred import AlfredMod, AlfredModActionEnum


class TestInitMethod:
    @pytest.mark.parametrize(
        "action, subtitle, arg, is_valid",
        [
            (AlfredModActionEnum.CMD, "subtitle", "arg", True),
            (AlfredModActionEnum.CMD, "subtitle", "arg", False),
        ],
    )
    def test_initial_data(self, action, subtitle, arg, is_valid):
        mod = AlfredMod(action=action, is_valid=is_valid, subtitle=subtitle, arg=arg)

        assert mod.action == action
        assert mod.is_valid == is_valid
        assert mod.subtitle == subtitle
        assert mod.arg == arg
        assert mod.variables == {}


class TestAddVariableMethod:
    def test_variables_updating(self):
        incoming_key, incoming_value = "key", "value"
        mod = AlfredMod(AlfredModActionEnum.CMD, "", "")
        mod.add_variable(incoming_key, incoming_value)

        assert mod.variables.get(incoming_key) == incoming_value

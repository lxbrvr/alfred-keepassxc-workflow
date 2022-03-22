import pytest

from conf import SettingsAttr


class TestInitMethod:
    @pytest.mark.parametrize(
        "incoming_env_name, incoming_cast_to, incoming_required, expected_env_name, expected_cast_to, expected_required",
        [
            ("env", None, False, "env", str, False),
            ("env", int, False, "env", int, False),
            ("env", None, True, "env", str, True),
        ],
    )
    def test_attributes_assigning(
        self,
        incoming_required,
        incoming_cast_to,
        incoming_env_name,
        expected_required,
        expected_env_name,
        expected_cast_to,
    ):
        settings_attr = SettingsAttr(
            env_name=incoming_env_name,
            cast_to=incoming_cast_to,
            required=incoming_required,
        )

        assert settings_attr._env_name == expected_env_name
        assert settings_attr._cast_func == expected_cast_to
        assert settings_attr.required == expected_required


class TestValueProperty:
    def test_when_there_is_empty_string_in_env(self, environ_factory):
        environ_factory(env="")
        settings_attr = SettingsAttr(env_name="env")

        assert settings_attr.value is None

    def test_when_there_is_no_env_variable(self):
        settings_attr = SettingsAttr(env_name="env")
        assert settings_attr.value is None

    def test_calling_of_cast_func(self, environ_factory, mocker):
        environ_factory(env="value")
        settings_attr = SettingsAttr(env_name="env")
        cast_func_mock = mocker.patch.object(settings_attr, "_cast_func")
        _ = settings_attr.value

        cast_func_mock.assert_called_once()


class TestRawValueProperty:
    def test_calling_os_getenv(self, mocker):
        getenv_mock = mocker.patch("conf.os.getenv")
        settings_attr = SettingsAttr(env_name="some_env")
        _ = settings_attr.raw_value

        getenv_mock.assert_called_once()

    def test_env_returning(self, environ_factory):
        env_value = "value"
        environ_factory(env=env_value)
        setting_attr = SettingsAttr(env_name="env")

        assert setting_attr.raw_value == env_value


class TestNameProperty:
    def test_result_value(self):
        env_value = "value"
        settings_attr = SettingsAttr(env_name=env_value)
        assert settings_attr.name == env_value

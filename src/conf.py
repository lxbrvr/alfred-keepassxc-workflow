import os
import typing as t

from helpers import cast_value_to_bool, split_string_with_commas


class SettingsException(Exception):
    pass


class RequiredFieldException(SettingsException):
    pass


class SettingsAttr:
    """Interface for working with setting attributes."""

    def __init__(self, env_name: str, cast_to: t.Callable[..., t.Any] = None, required: bool = False) -> None:
        self._env_name = env_name
        self._cast_func = cast_to or str
        self.required = required

    @property
    def value(self) -> t.Any:
        """
        Casts a raw value from environment variable to needed value.
        If there is no value in an environment variable or it is empty then
        returns None.
        """

        raw_value = self.raw_value

        if raw_value is None or raw_value == "":
            return None

        return self._cast_func(raw_value)

    @property
    def raw_value(self) -> t.Optional[str]:
        """Returns a value directly from an environment variable."""

        return os.getenv(self._env_name)

    @property
    def name(self) -> str:
        """Returns a name of environment variable"""

        return self._env_name


class SettingsMeta(type):
    def __new__(
        mcs: t.Type["SettingsMeta"], name: str, bases: t.Tuple[type, ...], attributes: t.Dict[str, t.Any]
    ) -> "SettingsMeta":
        cls = super().__new__(mcs, name, bases, attributes)

        cls.fields = []  # type: ignore

        for attr, obj in attributes.items():
            if isinstance(obj, SettingsAttr):
                cls.fields.append(obj)  # type: ignore

        return cls


class Settings(metaclass=SettingsMeta):
    """Class with global settings"""

    fields: t.List[SettingsAttr]

    ALFRED_KEYWORD = SettingsAttr(env_name="alfred_keyword", required=True)
    KEEPASSXC_CLI_PATH = SettingsAttr(env_name="keepassxc_cli_path", required=True)
    KEEPASSXC_DB_PATH = SettingsAttr(env_name="keepassxc_db_path", required=True)
    KEEPASSXC_MASTER_PASSWORD = SettingsAttr(env_name="keepassxc_master_password")
    KEEPASSXC_KEYFILE_PATH = SettingsAttr(env_name="keepassxc_keyfile_path")
    KEYCHAIN_ACCOUNT = SettingsAttr(env_name="keychain_account", required=True)
    KEYCHAIN_SERVICE = SettingsAttr(env_name="keychain_service", required=True)
    SHOW_ATTRIBUTE_VALUES = SettingsAttr(env_name="show_attribute_values", cast_to=cast_value_to_bool)
    SHOW_UNFILLED_ATTRIBUTES = SettingsAttr(env_name="show_unfilled_attributes", cast_to=cast_value_to_bool)
    DESIRED_ATTRIBUTES = SettingsAttr(env_name="desired_attributes", cast_to=split_string_with_commas)
    SHOW_PASSWORDS = SettingsAttr(env_name="show_passwords", cast_to=cast_value_to_bool)
    ENTRY_DELIMITER = SettingsAttr(env_name="entry_delimiter")
    PYTHON_PATH = SettingsAttr(env_name="python_path", required=True)
    SHOW_TOTP_REQUEST = SettingsAttr(env_name="show_totp_request", cast_to=cast_value_to_bool)
    CLIPBOARD_TIMEOUT = SettingsAttr(env_name="clipboard_timeout", cast_to=int)

    def validate(self) -> None:
        """
        Checks current values in settings fields.
        If it isn't valid then an exception will be raised.
        """

        for field in self.fields:
            if field.required and field.value is None:
                raise RequiredFieldException

    def is_valid(self) -> bool:
        """
        Checks settings values and returns a boolean value as result.
        Where True is valid settings, False is not.
        """

        try:
            self.validate()
        except RequiredFieldException:
            return False
        else:
            return True


settings = Settings()

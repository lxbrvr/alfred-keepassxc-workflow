import pytest
from contextlib2 import ExitStack

from conf import RequiredFieldException


class TestIsValidMethod(object):
    @pytest.mark.parametrize(
        "raised_exception, expected_result",
        [
            (RequiredFieldException, False),
            (lambda: None, True),
        ]
    )
    def test(self, raised_exception, expected_result, settings_factory, mocker):
        settings = settings_factory()
        mocker.patch.object(settings, "validate", side_effect=raised_exception)

        assert settings.is_valid() == expected_result


class TestValidateMethod(object):
    @pytest.mark.parametrize(
        "alfred_keyword, keepassxc_cli_path, keepassxc_db_path, keychain_account, keychain_service, expected_exception",
        [
            (None, None, None, None, None, pytest.raises(RequiredFieldException)),
            ("1", None, None, None, None, pytest.raises(RequiredFieldException)),
            ("1", "1", None, None, None, pytest.raises(RequiredFieldException)),
            ("1", "1", "1", None, None, pytest.raises(RequiredFieldException)),
            ("1", "1", "1", "1", None, pytest.raises(RequiredFieldException)),
            ("1", "1", "1", "1", "1", ExitStack()),
        ]
    )
    def test_required_attributes(
        self,
        settings_factory,
        alfred_keyword,
        keepassxc_db_path,
        keepassxc_cli_path,
        keychain_account,
        keychain_service,
        expected_exception,
    ):
        settings = settings_factory(
            alfred_keyword=alfred_keyword,
            keepassxc_cli_path=keepassxc_cli_path,
            keepassxc_db_path=keepassxc_db_path,
            keychain_service=keychain_service,
            keychain_account=keychain_account,
        )

        with expected_exception:
            settings.validate()

from services import initialize_keepassxc_client


class TestInitializeKeepassXCClient:
    def test_calls_with_parameters(self, mocker, valid_settings):
        keychain_access_mock = mocker.patch("services.KeychainAccess.get_password")
        kp_client_mock = mocker.patch("services.KeepassXCClient")

        initialize_keepassxc_client()

        keychain_access_mock.assert_called_with(
            account=valid_settings.KEYCHAIN_ACCOUNT.value,
            service=valid_settings.KEYCHAIN_SERVICE.value,
        )

        kp_client_mock.assert_called_with(
            cli_path=valid_settings.KEEPASSXC_CLI_PATH.value,
            db_path=valid_settings.KEEPASSXC_DB_PATH.value,
            key_file=valid_settings.KEEPASSXC_KEYFILE_PATH.value,
            password=keychain_access_mock(),
        )

    def test_returned_value(self, mocker):
        mocker.patch("services.KeychainAccess.get_password")
        kp_client_mock = mocker.patch("services.KeepassXCClient")
        actual_value = initialize_keepassxc_client()

        assert actual_value == kp_client_mock()

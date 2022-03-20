import subprocess

import pytest

from services import KeychainAccess


class TestGetPasswordMethod(object):
    @pytest.mark.parametrize(
        "keychain_output, expected_password",
        [
            (b"password: \n", ""),
            (b'password: "123123"', "123123"),
            (b"password: 0xD0BFD0B0D180D0BED0BBD18C", "пароль"),
            (b'password: 0x616263D0B0D0B1D0B2  "abc\320\260\320\261\320\262"', "abcабв"),
        ],
    )
    def test_passwords_parsing(self, keychain_account, keychain_service, mocker, keychain_output, expected_password):
        popen_mock = mocker.patch("services.subprocess.Popen")
        popen_mock.return_value.returncode = 0
        popen_mock.return_value.communicate.return_value = ("", keychain_output)
        service = KeychainAccess()
        password = service.get_password(account=keychain_account, service=keychain_service)

        assert password == expected_password

    def test_fail_code_from_keychain(self, mocker, keychain_account, keychain_service):
        popen_mock = mocker.patch("services.subprocess.Popen")
        popen_mock.return_value.returncode = 1
        popen_mock.return_value.communicate.return_value = ("", "")
        service = KeychainAccess()

        with pytest.raises(OSError):
            service.get_password(account=keychain_account, service=keychain_service)

    def test_called_os_command(self, mocker, keychain_account, keychain_service):
        popen_mock = mocker.patch("services.subprocess.Popen")
        popen_mock.return_value.returncode = 0
        popen_mock.return_value.communicate.return_value = ("", b'password: "password"')
        service = KeychainAccess()
        service.get_password(account=keychain_account, service=keychain_service)
        popen_mock.assert_called_with(
            ["security", "find-generic-password", "-g", "-a", keychain_account, "-s", keychain_service],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_password_parsing_with_incorrect_output(self, mocker, keychain_account, keychain_service):
        popen_mock = mocker.patch("services.subprocess.Popen")
        popen_mock.return_value.returncode = 0
        popen_mock.return_value.communicate.return_value = ("", b"")
        service = KeychainAccess()

        with pytest.raises(OSError):
            service.get_password(account=keychain_account, service=keychain_service)

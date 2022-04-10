import subprocess

import pytest

from services import KeepassXCClient


class TestInitMethod:
    def test_attributes(self):
        cli_path = "cli_path"
        db_path = "db_path"
        key_file = "key_file"
        password = "password"

        client = KeepassXCClient(
            cli_path=cli_path,
            db_path=db_path,
            key_file=key_file,
            password=password,
        )

        assert client.cli_path == cli_path
        assert client.db_path == db_path
        assert client.key_file == key_file
        assert client.password == password


class TestNormalizeQueryMethod:
    def test_normalization(self):
        pass


class TestBuildCommandMethod:
    @pytest.mark.parametrize(
        "key_file, password, action_parameters, expected_command",
        [
            (None, None, [], ["cli", "action", "-q", "db_path", "--no-password"]),
            (None, "password", [], ["cli", "action", "-q", "db_path"]),
            ("key_file", "password", [], ["cli", "action", "-q", "db_path", "-k", "key_file"]),
            ("key_file", "password", ["parameter"], ["cli", "action", "-q", "db_path", "parameter", "-k", "key_file"]),
        ],
    )
    def test_command_building(self, key_file, password, action_parameters, expected_command):
        client = KeepassXCClient(
            cli_path="cli",
            db_path="db_path",
            key_file=key_file,
            password=password,
        )

        actual_command = client._build_command(action="action", action_parameters=action_parameters)

        assert actual_command == expected_command


class TestRunCommandMethod:
    def test_with_non_successful_code(self, mocker, keepassxc_client):
        popen_mock = mocker.patch("services.subprocess.Popen")
        popen_mock.return_value.returncode = 1
        popen_mock.return_value.communicate.return_value = ("", "")

        with pytest.raises(OSError):
            command = ""
            keepassxc_client._run_command(command)

    def test_popen_parameters(self, mocker, keepassxc_client):
        popen_mock = mocker.patch("services.subprocess.Popen")
        popen_mock.return_value.returncode = 0
        popen_mock.return_value.communicate.return_value = (b"", b"")

        command = "command"
        keepassxc_client._run_command(command)

        popen_mock.assert_called_with(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
        popen_mock.assert_called_once()

    def test_output(self, mocker, keepassxc_client):
        popen_mock = mocker.patch("services.subprocess.Popen")
        popen_mock.return_value.returncode = 0
        expected_output = b"output"
        popen_mock.return_value.communicate.return_value = (expected_output, b"")
        command = "command"
        actual_output = keepassxc_client._run_command(command)

        assert actual_output == "output"


class TestShowMethod:
    def test_build_command_parameters(self, keepassxc_client, mocker):
        build_command_mock = mocker.patch.object(keepassxc_client, "_build_command")
        mocker.patch.object(keepassxc_client, "_run_command")
        incoming_query = "query"
        keepassxc_client.show(incoming_query)

        build_command_mock.assert_called_with(
            action="show",
            action_parameters=[
                "-a",
                "title",
                "-a",
                "username",
                "-a",
                "password",
                "-a",
                "url",
                "-a",
                "notes",
                incoming_query,
            ],
        )

    def test_run_command(self, keepassxc_client, mocker):
        build_command_mock = mocker.patch.object(keepassxc_client, "_build_command")
        run_command_mock = mocker.patch.object(keepassxc_client, "_run_command")
        keepassxc_client.show("query")

        run_command_mock.assert_called_with(build_command_mock())

    @pytest.mark.parametrize(
        "command_output, expected_title, expected_username, expected_password, expected_url, expected_notes",
        [
            (
                "title\nusername\npassword\nurl\nthis\nis\nnotes\n",
                "title",
                "username",
                "password",
                "url",
                "this\nis\nnotes",
            ),
            (
                "\n\n\n\n\n",
                "",
                "",
                "",
                "",
                "",
            ),
            (
                "title\n\n\n\n\n",
                "title",
                "",
                "",
                "",
                "",
            ),
            (
                "\nusername\n\n\n\n",
                "",
                "username",
                "",
                "",
                "",
            ),
            (
                "\n\npassword\n\n\n",
                "",
                "",
                "password",
                "",
                "",
            ),
            (
                "\n\n\nurl\n\n",
                "",
                "",
                "",
                "url",
                "",
            ),
            (
                "\n\n\n\nnotes\n",
                "",
                "",
                "",
                "",
                "notes",
            ),
            (
                "\n\n\n\nthis\nis\nnotes\n",
                "",
                "",
                "",
                "",
                "this\nis\nnotes",
            ),
        ],
    )
    def test_parsing_of_command_output(
        self,
        keepassxc_client,
        mocker,
        command_output,
        expected_title,
        expected_username,
        expected_password,
        expected_url,
        expected_notes,
    ):
        mocker.patch.object(keepassxc_client, "_build_command")
        mocker.patch.object(keepassxc_client, "_run_command", return_value=command_output)
        actual_keepassxc_item = keepassxc_client.show("query")

        assert actual_keepassxc_item.title == expected_title
        assert actual_keepassxc_item.username == expected_username
        assert actual_keepassxc_item.password == expected_password
        assert actual_keepassxc_item.url == expected_url
        assert actual_keepassxc_item.notes == expected_notes


class TestSearchMethod:
    def test_build_command_parameters(self, keepassxc_client, mocker):
        build_command_mock = mocker.patch.object(keepassxc_client, "_build_command")
        mocker.patch.object(keepassxc_client, "_run_command")
        incoming_query = "query"
        keepassxc_client.search(incoming_query)

        build_command_mock.assert_called_with(
            action="search",
            action_parameters=[incoming_query],
        )

    def test_run_command(self, keepassxc_client, mocker):
        build_command_mock = mocker.patch.object(keepassxc_client, "_build_command")
        run_command_mock = mocker.patch.object(keepassxc_client, "_run_command")
        keepassxc_client.search("query")

        run_command_mock.assert_called_with(build_command_mock())

    @pytest.mark.parametrize(
        "command_output, expected_result",
        [("entry1\nentry2\n", ["entry1", "entry2"]), ("entry1\n", ["entry1"]), ("запись\n", ["запись"])],
    )
    def test_parsing_of_command_output(self, keepassxc_client, mocker, command_output, expected_result):
        mocker.patch.object(keepassxc_client, "_build_command")
        mocker.patch.object(keepassxc_client, "_run_command", return_value=command_output)
        actual_result = keepassxc_client.search("query")

        assert actual_result == expected_result


class TestTotpMethod:
    def test_build_command_parameters(self, keepassxc_client, mocker):
        build_command_mock = mocker.patch.object(keepassxc_client, "_build_command")
        mocker.patch.object(keepassxc_client, "_run_command")
        incoming_query = "query"
        keepassxc_client.totp(incoming_query)

        build_command_mock.assert_called_with(
            action="show",
            action_parameters=["-t", incoming_query],
        )

    def test_run_command(self, keepassxc_client, mocker):
        build_command_mock = mocker.patch.object(keepassxc_client, "_build_command")
        run_command_mock = mocker.patch.object(keepassxc_client, "_run_command")
        keepassxc_client.totp("query")

        run_command_mock.assert_called_with(build_command_mock())

    def test_parsing_of_command_output(self, keepassxc_client, mocker):
        actual_output = "123\n"
        expected_result = "123"
        mocker.patch.object(keepassxc_client, "_build_command")
        mocker.patch.object(keepassxc_client, "_run_command", return_value=actual_output)
        actual_result = keepassxc_client.totp("query")

        assert actual_result == expected_result

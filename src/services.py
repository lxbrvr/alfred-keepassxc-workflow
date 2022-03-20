import typing as t
import binascii
import re
import subprocess
import unicodedata

from conf import settings


class KeepassXCItem:
    """Representations class for a KeepassXC entry. """

    def __init__(self, title: str, username: str, password: str, url: str, notes: str) -> None:
        self.title = title
        self.username = username
        self.password = password
        self.url = url
        self.notes = notes

    @staticmethod
    def is_empty(value: str) -> bool:
        """Returns True if an entry attribute has the None value or the empty string"""

        return value is None or value == ""


class KeychainAccess:
    """interface for security system command."""

    @staticmethod
    def get_password(account: str, service: str) -> str:
        """Returns a password using "security find-generic-password" command."""

        command = ["security", "find-generic-password", "-g", "-a", account, "-s", service]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            error = (
                "Can't fetch a password from security tool.\n"
                "Exit code: {exit_code}.\n"
                "Output: {output}"
            )
            raise OSError(error.format(output=stderr, exit_code=process.returncode))

        output = stderr.decode("utf-8")

        if output == "password: \n":  # there is no password
            return ""

        matches = re.search(r"password:\s*(?:0x(?P<hex>[0-9A-F]+)\s*)?(?:\"(?P<password>.*)\")?", output)

        if not matches:
            raise OSError("Can't parse the master password from output of secure command.")

        groups = matches.groupdict()
        password_hex = groups.get("hex")

        if password_hex:
            return binascii.unhexlify(password_hex).decode("utf-8")

        return groups.get("password", "")


class KeepassXCClient:
    """Interface for keepassxc-cli system command."""

    def __init__(self, cli_path: str, db_path: str, key_file: str, password: str) -> None:
        self.cli_path = cli_path
        self.db_path = db_path
        self.key_file = key_file
        self.password = password

    def _normalize_query(self, query: str) -> str:
        query = unicodedata.normalize("NFKC", query)
        return query

    def _build_command(self, action: str, action_parameters: t.List[str]) -> t.List[str]:
        command = [self.cli_path, action, "-q", self.db_path]
        command += action_parameters

        if self.key_file:
            command += ["-k", self.key_file]

        if not self.password:
            command += ["--no-password"]

        command = [self._normalize_query(arg) for arg in command]

        return command

    def _run_command(self, command: t.List[str]) -> str:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
        output, _ = process.communicate(input=self.password.encode())

        if process.returncode != 0:
            error = (
                "Can't fetch data from keepassxc-cli tool.\n"
                "Exit code: {exit_code}.\n"
            )
            raise OSError(error.format(output=output, exit_code=process.returncode))

        return str(output)

    def show(self, query: str) -> KeepassXCItem:
        """Handles the system command "keepassxc-cli show"."""

        cmd_parameters = "-a title -a username -a password -a url -a notes".split(" ")
        cmd_parameters += [query]
        command = self._build_command(action="show", action_parameters=cmd_parameters)
        output = self._run_command(command)
        entry_data = output[:-1].split("\n")  # the latest element is break line

        return KeepassXCItem(
            title=entry_data[0],
            username=entry_data[1],
            password=entry_data[2],
            url=entry_data[3],
            notes="\n".join(entry_data[4:]),
        )

    def locate(self, query: str) -> t.List[str]:
        """Handles the system command "keepassxc-cli locate"."""

        command = self._build_command(action="locate", action_parameters=[query])
        output = self._run_command(command)

        return output.split("\n")[:-1]  # the latest element is empty string


def initialize_keepassxc_client() -> KeepassXCClient:
    """Initializes the KeepassXC client using user settings."""

    password = KeychainAccess().get_password(
        account=settings.KEYCHAIN_ACCOUNT.value,
        service=settings.KEYCHAIN_SERVICE.value,
    )

    kp_client = KeepassXCClient(
        cli_path=settings.KEEPASSXC_CLI_PATH.value,
        db_path=settings.KEEPASSXC_DB_PATH.value,
        key_file=settings.KEEPASSXC_KEYFILE_PATH.value,
        password=password,
    )

    return kp_client

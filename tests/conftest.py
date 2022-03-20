import plistlib

import pytest

from alfred import AlfredScriptFilter
from conf import Settings
from services import KeepassXCClient, KeepassXCItem


@pytest.fixture
def info_plist():
    return plistlib.readPlist("src/info.plist")


@pytest.fixture
def keychain_account():
    yield "account"


@pytest.fixture
def keychain_service():
    yield "service"


@pytest.fixture
def keepassxc_item():
    yield KeepassXCItem(
        title="title",
        username="username",
        password="password",
        url="url",
        notes="notes",
    )


@pytest.fixture
def alfred_script_filter():
    yield AlfredScriptFilter()


@pytest.fixture
def environ_factory(mocker):
    def create(**kw):
        mocker.patch.dict("conf.os.environ", {k: v for k, v in kw.items() if v is not None})
    yield create


@pytest.fixture
def settings_factory(environ_factory):
    def create(**kw):
        environ_factory(**kw)
        return Settings()
    yield create


@pytest.fixture
def invalid_settings(settings_factory):
    yield settings_factory()


@pytest.fixture
def valid_settings(settings_factory, keychain_service, keychain_account):
    yield settings_factory(
        alfred_keyword="kp",
        keepassxc_db_path="/db/path",
        keepassxc_cli_path="/cli/path",
        keepassxc_master_password="******",
        keychain_service=keychain_service,
        keychain_account=keychain_account,
        entry_delimiter=" > ",
        desired_attributes="title,username,password",
    )


@pytest.fixture
def configurable_valid_settings(settings_factory, keychain_service, keychain_account):
    def wrapper(**kw):
        settings = {
            "alfred_keyword": "kp",
            "keepassxc_db_path": "/db/path",
            "keepassxc_cli_path": "/cli/path",
            "keepassxc_master_password": "******",
            "keychain_service": keychain_service,
            "keychain_account": keychain_account,
            "entry_delimiter": " > ",
        }
        settings.update(**kw)

        return settings_factory(**settings)

    yield wrapper


@pytest.fixture
def keepassxc_client():
    yield KeepassXCClient(
        cli_path="/cli/path",
        db_path="/db/path",
        key_file="/key/path",
        password="password",
    )

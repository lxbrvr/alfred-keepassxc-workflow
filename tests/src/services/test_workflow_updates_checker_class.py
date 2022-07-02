import json

import pytest

from helpers import Version
from services import WorkflowUpdatesChecker


class TestInitMethod:
    def test_init_values(self):
        checker = WorkflowUpdatesChecker()

        assert checker._cached_latest_version is None


class TestCurrentValueProperty:
    def test_returned_value(self, version_factory, mocker):
        alfred_workflow_version = "1.2.3"
        checker = WorkflowUpdatesChecker()
        mocker.patch.dict("services.os.environ", {"alfred_workflow_version": alfred_workflow_version})

        assert checker.current_version == version_factory(alfred_workflow_version)


class TestFetchLatestVersion:
    def test_cache(self, mocker, version_factory):
        checker = WorkflowUpdatesChecker()
        version = "1.0.0"
        response = mocker.MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps({"tag_name": version})
        mocker.patch("services.urllib.request.urlopen", return_value=response)
        first_fetched_version = checker.fetch_latest_version()
        response = mocker.MagicMock()
        response.__enter__.return_value.read.return_value = {"tag_name": "2.0.0"}
        mocker.patch("services.urllib.request.urlopen", return_value=response)
        second_fetched_version = checker.fetch_latest_version()

        assert version_factory(version) == first_fetched_version == second_fetched_version

    def test_called_openurl(self, mocker):
        urlopen_mock = mocker.patch("services.urllib.request.urlopen")
        mocker.patch("services.json.loads")
        checker = WorkflowUpdatesChecker()
        checker.fetch_latest_version()

        urlopen_mock.assert_called_once_with(
            "https://api.github.com/repos/lxbrvr/alfred-keepassxc-workflow/releases/latest",
            timeout=10,
        )

    def test_result(self, version_factory, mocker):
        checker = WorkflowUpdatesChecker()
        version = "1.0.0"
        response = mocker.MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps({"tag_name": version})
        mocker.patch("services.urllib.request.urlopen", return_value=response)
        actual_version = checker.fetch_latest_version()
        expected_version = version_factory(version)

        assert actual_version == expected_version


class TestHasNewVersionMethod:
    @pytest.mark.parametrize(
        "current_version, latest_version, is_new_version",
        [
            (Version("1.0.0"), Version("1.0.0"), False),
            (Version("1.0.0"), Version("1.0.1"), True),
            (Version("1.0.0"), Version("0.0.1"), False),
        ],
    )
    def test_versions_combo(self, current_version, latest_version, is_new_version, version_factory, mocker):
        mocker.patch.multiple(
            WorkflowUpdatesChecker,
            current_version=mocker.PropertyMock(return_value=current_version),
            fetch_latest_version=mocker.Mock(return_value=latest_version),
        )

        checker = WorkflowUpdatesChecker()

        assert checker.has_new_version() == is_new_version

    def test_versions_combo_with_ignored_skipped_version(self, version_factory, mocker):
        mocker.patch.multiple(
            WorkflowUpdatesChecker,
            current_version=mocker.PropertyMock(return_value="1.0.0"),
            fetch_latest_version=mocker.Mock(return_value="2.0.0"),
        )

        checker = WorkflowUpdatesChecker()

        assert checker.has_new_version()

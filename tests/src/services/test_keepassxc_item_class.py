import pytest

from services import KeepassXCItem


class TestInitMethod(object):
    def test_class_attributes(self):
        title = "title"
        password = "password"
        url = "url"
        notes = "notes"
        username = "username"

        item = KeepassXCItem(title=title, username=username, password=password, notes=notes, url=url)

        assert item.title == title
        assert item.username == username
        assert item.url == url
        assert item.notes == notes
        assert item.password == password


class TestIsEmptyMethod(object):
    @pytest.mark.parametrize(
        "value, is_empty",
        [
            (None, True),
            ("", True),
            ("data", False),
        ],
    )
    def test_is_empty(self, keepassxc_item, value, is_empty):
        assert keepassxc_item.is_empty(value) == is_empty

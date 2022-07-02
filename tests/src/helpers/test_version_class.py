import pytest

from helpers import Version


class TestInitMethod:
    def test_initial_parameters(self):
        raw_version = "1.2.3"
        version = Version(raw_version)

        assert version.raw_version == raw_version


class TestRawProperty:
    def test_returned_value(self, version_factory):
        version = version_factory()
        assert version.raw_version == version.raw


class TestTupleMethod:
    def test_returned_value(self):
        version = Version("1.2.3")
        assert version.tuple == (1, 2, 3)


class TestLtMagicMethod:
    @pytest.mark.parametrize(
        "first_version, second_version, is_first_lt_second",
        [
            ("1.0.0", "1.0.1", True),
            ("1.0.0", "1.0.0", False),
            ("1.0.0", "1.1.0", True),
            ("1.0.0", "2.0.0", True),
            ("1.0.0", "0.0.1", False),
            ("1.0.0", "0.1.0", False),
        ],
    )
    def test_comparison(self, version_factory, first_version, second_version, is_first_lt_second):
        actual_result = version_factory(first_version) < version_factory(second_version)
        assert actual_result == is_first_lt_second


class TestGtMagicMethod:
    @pytest.mark.parametrize(
        "first_version, second_version, is_first_gt_second",
        [
            ("1.0.0", "1.0.1", False),
            ("1.0.0", "1.0.0", False),
            ("1.0.0", "1.1.0", False),
            ("1.0.0", "2.0.0", False),
            ("1.0.0", "0.0.1", True),
            ("1.0.0", "0.1.0", True),
        ],
    )
    def test_comparison(self, version_factory, first_version, second_version, is_first_gt_second):
        actual_result = version_factory(first_version) > version_factory(second_version)
        assert actual_result == is_first_gt_second


class TestEqMagicMethod:
    @pytest.mark.parametrize(
        "first_version, second_version, is_first_eq_second",
        [
            ("1.0.0", "1.0.1", False),
            ("1.0.0", "1.0.0", True),
            ("1.0.0", "1.1.0", False),
            ("1.0.0", "2.0.0", False),
            ("1.0.0", "0.0.1", False),
            ("1.0.0", "0.1.0", False),
        ],
    )
    def test_comparison(self, version_factory, first_version, second_version, is_first_eq_second):
        actual_result = version_factory(first_version) == version_factory(second_version)
        assert actual_result == is_first_eq_second

    def test_with_another_object(self, version_factory):
        version = version_factory()
        assert version != 1

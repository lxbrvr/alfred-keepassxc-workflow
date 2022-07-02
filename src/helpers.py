import typing as t


def cast_value_to_bool(value: str) -> bool:
    """Casts a passed value to boolean value."""

    if isinstance(value, str):
        return value.lower() in ["1", "true", "yes"]

    if isinstance(value, bool):
        return value

    return False


def split_string_with_commas(value: str) -> t.List[str]:
    """
    Splits a passed value to a list. The comma is delimiter.
    Note all whitespaces will be removed before the splitting.

    Example:
        incoming value "a, b, c"
        output value ["a", "b", "c"]
    """

    return value.replace(" ", "").split(",") if value else []


def cast_bool_to_yesno(value: bool) -> str:
    """Returns "Yes" if a passed boolean value is True else False."""

    return "Yes" if value is True else "No"


class Version:
    """Provides the interface for working with semantic versions."""

    def __init__(self, version: str) -> None:
        self.raw_version = version

    @property
    def raw(self) -> str:
        """Returns the version as it was passed."""

        return self.raw_version

    @property
    def tuple(self) -> t.Tuple[int, int, int]:
        """Converts the raw version to numerical tuple."""

        major, minor, patch = self.raw_version.split(".")
        return int(major), int(minor), int(patch)

    def __gt__(self, other: "Version") -> bool:
        return self.tuple > other.tuple

    def __lt__(self, other: "Version") -> bool:
        return self.tuple < other.tuple

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return self.tuple == other.tuple

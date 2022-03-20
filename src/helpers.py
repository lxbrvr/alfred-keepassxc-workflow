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

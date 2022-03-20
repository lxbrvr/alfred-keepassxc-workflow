import json
import sys
import typing as t


class AlfredModActionEnum:
    CMD = "cmd"


class AlfredMod:
    """Class describing the modifier key in Alfred."""

    def __init__(self, action: AlfredModActionEnum, subtitle: str, arg: str, is_valid: bool = True) -> None:
        self.action = action
        self.is_valid = is_valid
        self.subtitle = subtitle
        self.arg = arg
        self.variables: t.Dict[str, str] = {}

    def add_variable(self, key: str, value: str) -> None:
        """Adds a passed variable to "variables" key for the Alfred's script filter item."""

        self.variables[key] = value


class AlfredScriptFilter:
    """Interface for working with the Alfred's script filter."""

    def __init__(self) -> None:
        self.items: t.List[t.Dict[str, t.Any]] = []
        self.variables: t.Dict[str, str] = {}

    def add_variable(self, key: str, value: str) -> None:
        """Adds a passed variable to "variables" key for the Alfred's script filter."""

        self.variables[key] = value

    def add_item(
        self,
        title: str,
        subtitle: t.Optional[str] = None,
        is_valid: bool = True,
        arg: t.Optional[str] = None,
        mods: t.Optional[t.List[AlfredMod]] = None,
    ) -> None:
        """
        Forms item data with specific format for the Alfred's script filter
        and adds to "items" key.
        """

        prepared_mods = {
            i.action: {"subtitle": i.subtitle, "valid": i.is_valid, "arg": i.arg, "variables": i.variables}
            for i in mods or []
        } or None

        item = {
            "title": title,
            "subtitle": subtitle,
            "valid": is_valid,
            "arg": arg,
            "mods": prepared_mods,
        }

        item = {k: v for k, v in item.items() if v is not None}
        self.items.append(item)

    def send(self) -> None:
        """
        Writes a collected data to stdout as json.
        This output will be parsed by the Alfred's script filter.
        """

        data: t.Dict[str, t.Any] = {"items": self.items}

        if self.variables:
            data["variables"] = self.variables

        json.dump(data, sys.stdout)
        sys.stdout.flush()

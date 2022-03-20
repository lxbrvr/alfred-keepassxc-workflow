import json
import sys


class AlfredModActionEnum:
    CMD = "cmd"


class AlfredMod:
    """Class describing the modifier key in Alfred."""

    def __init__(self, action, subtitle, arg, is_valid=True):
        self.action = action
        self.is_valid = is_valid
        self.subtitle = subtitle
        self.arg = arg
        self.variables = {}

    def add_variable(self, key, value):
        """Adds a passed variable to "variables" key for the Alfred's script filter item."""

        self.variables[key] = value


class AlfredScriptFilter:
    """Interface for working with the Alfred's script filter."""

    def __init__(self):
        self.items = []
        self.variables = {}

    def add_variable(self, key, value):
        """Adds a passed variable to "variables" key for the Alfred's script filter."""

        self.variables[key] = value

    def add_item(self, title, subtitle=None, is_valid=True, arg=None, mods=None):
        """
        Forms item data with specific format for the Alfred's script filter
        and adds to "items" key.
        """

        prepared_mods = {
            i.action: {
                "subtitle": i.subtitle,
                "valid": i.is_valid,
                "arg": i.arg,
                "variables": i.variables
            } for i in mods or []
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

    def send(self):
        """
        Writes a collected data to stdout as json.
        This output will be parsed by the Alfred's script filter.
        """

        data = {"items": self.items}

        if self.variables:
            data["variables"] = self.variables

        json.dump(data, sys.stdout)
        sys.stdout.flush()

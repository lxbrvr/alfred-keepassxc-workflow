import json
import sys


class AlfredScriptFilter:
    """Interface for working with the Alfred's script filter."""

    def __init__(self):
        self.items = []
        self.variables = {}

    def add_variable(self, key, value):
        """Adds a passed variable to "variables" key for the Alfred's script filter."""

        self.variables[key] = value

    def add_item(self, title, subtitle=None, is_valid=True, arg=None):
        """
        Forms item data with specific format for the Alfred's script filter
        and adds to "items" key.
        """

        item = {"title": title, "subtitle": subtitle, "valid": is_valid, "arg": arg}
        item = {k: v for k, v in item.iteritems() if v is not None}
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

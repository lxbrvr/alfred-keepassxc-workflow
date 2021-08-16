import argparse
import traceback

from handlers import fetch_handler, list_settings_handler, search_handler


class CLIActions(object):
    SEARCH = "search"
    FETCH = "fetch"
    SETTINGS_LIST = "settings_list"

    @classmethod
    def choices(cls):
        """Returns an action list."""

        return [
            cls.SEARCH,
            cls.FETCH,
            cls.SETTINGS_LIST,
        ]


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    search_parse = subparsers.add_parser(CLIActions.SEARCH)
    search_parse.set_defaults(handler=search_handler, action=CLIActions.SEARCH)
    search_parse.add_argument("query")

    fetch_parser = subparsers.add_parser(CLIActions.FETCH)
    fetch_parser.set_defaults(handler=fetch_handler, action=CLIActions.FETCH)
    fetch_parser.add_argument("query")

    settings_list_parser = subparsers.add_parser(CLIActions.SETTINGS_LIST)
    settings_list_parser.set_defaults(handler=list_settings_handler)

    return parser.parse_args()


def main():
    parsed_args = parse_args()

    try:
        parsed_args.handler(parsed_args)
    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    main()

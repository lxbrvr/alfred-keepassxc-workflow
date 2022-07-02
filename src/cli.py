import argparse
import traceback
import typing as t

from handlers import (
    check_for_updates_handler,
    fetch_handler,
    list_settings_handler,
    search_handler,
    totp_handler,
)


class CLIActions:
    SEARCH = "search"
    FETCH = "fetch"
    SETTINGS_LIST = "settings_list"
    TOTP = "totp"
    CHECK_FOR_UPDATES = "check_for_updates"

    @classmethod
    def choices(cls) -> t.List[str]:
        """Returns an action list."""

        return [cls.SEARCH, cls.FETCH, cls.SETTINGS_LIST, cls.TOTP, cls.CHECK_FOR_UPDATES]


def parse_args() -> argparse.Namespace:
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

    totp_parser = subparsers.add_parser(CLIActions.TOTP)
    totp_parser.set_defaults(handler=totp_handler)
    totp_parser.add_argument("query")

    check_for_updates_parser = subparsers.add_parser(CLIActions.CHECK_FOR_UPDATES)
    check_for_updates_parser.set_defaults(handler=check_for_updates_handler)

    return parser.parse_args()


def main() -> None:
    parsed_args = parse_args()

    try:
        parsed_args.handler(parsed_args)
    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    main()

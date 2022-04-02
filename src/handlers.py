import argparse
import typing as t

from alfred import AlfredMod, AlfredModActionEnum, AlfredScriptFilter
from conf import settings
from helpers import cast_bool_to_yesno
from services import initialize_keepassxc_client


def require_password(func: t.Callable[..., None]) -> t.Callable[..., None]:
    """Requires a password.

    If there is no password, the missing password notification item will
    be displayed in Alfred. When an user selects this item, he will be
    prompted to enter a new password. So it is necessary to send the arg
    with settings.KEEPASSXC_MASTER_PASSWORD.name value. It will be passed
    to js script as parameter.
    """

    def wrapper(*args, **kw):
        script_filter = AlfredScriptFilter()

        if settings.KEEPASSXC_MASTER_PASSWORD.value:
            return func(*args, **kw)

        script_filter.add_item(
            title="Please enter your password",
            subtitle="Press to open a dialog window",
            arg=settings.KEEPASSXC_MASTER_PASSWORD.name,
        )

        script_filter.send()

    return wrapper


def validate_settings(func: t.Callable[..., None]) -> t.Callable[..., None]:
    """
    Checks settings before a wrapped func calling.
    If there are some errors then it will notify an user.
    """

    def wrapper(*args, **kw):
        if settings.is_valid():
            return func(*args, **kw)

        script_filter = AlfredScriptFilter()

        script_filter.add_item(
            title="Express initialization", subtitle="Press to go to express initialization", arg="express"
        )

        script_filter.add_item(
            title="Configure your settings",
            subtitle="Press to go to settings.",
            arg="settings",
        )

        script_filter.send()

    return wrapper


@validate_settings
@require_password
def search_handler(parsed_args: argparse.Namespace) -> None:
    """
    Forms a list with found KeepassXC entries by a passed query
    and send it to the Alfred's script filter.
    """

    script_filter = AlfredScriptFilter()
    kp_client = initialize_keepassxc_client()

    try:
        kp_entries = kp_client.search(parsed_args.query)
    except OSError:
        script_filter.add_item(title="There aren't matches or something went wrong.", is_valid=False)
        script_filter.send()
        raise

    for entry_path in kp_entries:
        formatted_entry_path = entry_path[1:].replace("/", settings.ENTRY_DELIMITER.value)
        script_filter.add_item(title=formatted_entry_path, arg=entry_path)

    script_filter.add_variable("USER_QUERY", parsed_args.query)  # used for "back" button
    script_filter.send()


@validate_settings
@require_password
def fetch_handler(parsed_args: argparse.Namespace) -> None:
    """Forms a list with KeepassXC entry attributes and send it to the Alfred's script filter."""

    script_filter = AlfredScriptFilter()
    kp_client = initialize_keepassxc_client()
    kp_entry = kp_client.show(parsed_args.query)
    script_filter.add_item(title="← Back", subtitle="Back to search", arg="back")

    for desired_attr in settings.DESIRED_ATTRIBUTES.value:
        entry_value = getattr(kp_entry, desired_attr.strip())

        if not settings.SHOW_UNFILLED_ATTRIBUTES.value and kp_entry.is_empty(entry_value):
            continue

        subtitle = entry_value

        if desired_attr == "password" and not settings.SHOW_PASSWORDS.value:
            subtitle = "••••••••"

        title = desired_attr.title()
        title += " (empty)" if kp_entry.is_empty(entry_value) else ""
        subtitle = subtitle if settings.SHOW_ATTRIBUTE_VALUES.value else None
        is_valid = False if kp_entry.is_empty(entry_value) else True
        mod = AlfredMod(action=AlfredModActionEnum.CMD, subtitle="Copy and paste to front most app.", arg=entry_value)
        mod.add_variable("USER_ACTION", "mod")
        script_filter.add_item(title=title, subtitle=subtitle, is_valid=is_valid, arg=entry_value, mods=[mod])

    script_filter.send()


def list_settings_handler(_: argparse.Namespace) -> None:  # _ - it's parsed args without usage
    """Collects a list with global settings and sends it for the Alfred's script filter."""

    script_filter = AlfredScriptFilter()

    script_filter.add_item(
        title="Keyword name for Alfred's workflow",
        subtitle=settings.ALFRED_KEYWORD.raw_value,
        arg=settings.ALFRED_KEYWORD.name,
    )

    script_filter.add_item(
        title="KeepassXC database",
        subtitle=settings.KEEPASSXC_DB_PATH.raw_value,
        arg=settings.KEEPASSXC_DB_PATH.name,
    )

    script_filter.add_item(
        title="KeepassXC master password",
        subtitle=settings.KEEPASSXC_MASTER_PASSWORD.raw_value,
        arg=settings.KEEPASSXC_MASTER_PASSWORD.name,
    )

    script_filter.add_item(
        title="KeepassXC key file",
        subtitle=settings.KEEPASSXC_KEYFILE_PATH.raw_value,
        arg=settings.KEEPASSXC_KEYFILE_PATH.name,
    )

    script_filter.add_item(
        title="Display attribute values of KeepassXC records",
        subtitle=cast_bool_to_yesno(settings.SHOW_ATTRIBUTE_VALUES.value),
        arg=settings.SHOW_ATTRIBUTE_VALUES.name,
    )

    script_filter.add_item(
        title="Display blank attributes of KeepassXC records",
        subtitle=cast_bool_to_yesno(settings.SHOW_UNFILLED_ATTRIBUTES.value),
        arg=settings.SHOW_UNFILLED_ATTRIBUTES.name,
    )

    script_filter.add_item(
        title="Attributes of KeepassXC records to display",
        subtitle=(
            settings.DESIRED_ATTRIBUTES.raw_value.replace(",", ", ")
            if settings.DESIRED_ATTRIBUTES.raw_value
            else settings.DESIRED_ATTRIBUTES.raw_value
        ),
        arg=settings.DESIRED_ATTRIBUTES.name,
    )

    script_filter.add_item(
        title="Display real passwords of KeepassXC records",
        subtitle=cast_bool_to_yesno(settings.SHOW_PASSWORDS.value),
        arg=settings.SHOW_PASSWORDS.name,
    )

    script_filter.add_item(
        title="Delimiter in KeepassXC records list",
        subtitle=settings.ENTRY_DELIMITER.raw_value,
        arg=settings.ENTRY_DELIMITER.name,
    )

    script_filter.add_item(
        title="KeepassXC CLI path",
        subtitle=settings.KEEPASSXC_CLI_PATH.raw_value,
        arg=settings.KEEPASSXC_CLI_PATH.name,
    )

    script_filter.add_item(
        title="Keychain account name",
        subtitle=settings.KEYCHAIN_ACCOUNT.raw_value,
        arg=settings.KEYCHAIN_ACCOUNT.name,
    )

    script_filter.add_item(
        title="Keychain service name",
        subtitle=settings.KEYCHAIN_SERVICE.raw_value,
        arg=settings.KEYCHAIN_SERVICE.name,
    )

    script_filter.add_item(
        title="Python path",
        subtitle=settings.PYTHON_PATH.raw_value,
        arg=settings.PYTHON_PATH.name,
    )

    script_filter.send()

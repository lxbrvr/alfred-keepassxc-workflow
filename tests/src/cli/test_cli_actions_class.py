from cli import CLIActions


class TestChoicesMethod:
    actual_choices = CLIActions.choices()
    expected_choices = [
        CLIActions.SEARCH,
        CLIActions.FETCH,
        CLIActions.SETTINGS_LIST,
        CLIActions.TOTP,
        CLIActions.CHECK_FOR_UPDATES,
        CLIActions.OPEN_URL,
    ]

    assert actual_choices == expected_choices

from cli import CLIActions


class TestChoicesMethod:
    actual_choices = CLIActions.choices()
    expected_choices = [CLIActions.SEARCH, CLIActions.FETCH, CLIActions.SETTINGS_LIST]

    assert actual_choices == expected_choices

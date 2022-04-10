from cli import CLIActions, main, parse_args


class TestMain:
    def test_exception(self, mocker):
        namespace_mock = mocker.patch("argparse.Namespace")
        namespace_mock.handler.side_effect = Exception
        mocker.patch("cli.parse_args", return_value=namespace_mock)
        print_exc_mock = mocker.patch("cli.traceback.print_exc")
        main()

        print_exc_mock.assert_called_once()

    def test_without_exception(self, mocker):
        namespace_mock = mocker.patch("argparse.Namespace")
        mocker.patch("cli.parse_args", return_value=namespace_mock)
        print_exc_mock = mocker.patch("cli.traceback.print_exc")
        main()

        print_exc_mock.assert_not_called()


class TestParseArgs:
    def test_subparsers_parameters(self, mocker):
        add_parser_mock = mocker.patch("argparse._SubParsersAction.add_parser")
        mocker.patch("cli.argparse.ArgumentParser.parse_args")
        parse_args()

        add_parser_mock.assert_any_call(CLIActions.SEARCH)
        add_parser_mock.assert_any_call(CLIActions.SETTINGS_LIST)
        add_parser_mock.assert_any_call(CLIActions.FETCH)
        add_parser_mock.assert_any_call(CLIActions.TOTP)

        assert add_parser_mock.call_count == 4

from conf import SettingsAttr, SettingsMeta


class TestNewMethod(object):
    def test_attributes(self):
        expected_settings_attr = SettingsAttr(env_name="some_env")
        cls = SettingsMeta(
            "Settings",
            (object,),
            {
                "settings_attr": expected_settings_attr,
                "another_attr": "some_value",
            },
        )

        assert cls.fields == [expected_settings_attr]

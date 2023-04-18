from cmsplugin_blocks import defaults as default_settings
from cmsplugin_blocks.contrib.django_configuration import CmsBlocksDefaultSettings


def test_configuration_default_settings(settings):
    """
    Settings class should have attributes for each setting from default base ones and
    with the same value.
    """
    configuration_defaults = CmsBlocksDefaultSettings()

    # Get setting names from base module
    base_setting_names = [
        attr
        for attr in dir(default_settings)
        if not attr.startswith("_") and attr.isupper()
    ]

    # Get setting names from class
    configuration_setting_names = [
        attr
        for attr in dir(CmsBlocksDefaultSettings)
        if not attr.startswith("_") and attr.isupper()
    ]

    # Ensure class define every base names
    for item in base_setting_names:
        assert hasattr(configuration_defaults, item) is True

    # Ensure class does not define names that are not in base
    for item in configuration_setting_names:
        assert hasattr(default_settings, item) is True

    # Ensure all settings have the same value
    for item in configuration_setting_names:
        assert getattr(default_settings, item) == getattr(
            CmsBlocksDefaultSettings,
            item
        )

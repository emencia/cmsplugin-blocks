from django.apps import AppConfig


class CmspluginBlocks_Config(AppConfig):
    name = "cmsplugin_blocks"
    verbose_name = "CMS Blocks"
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        """
        Perform some validation on application loading
        """
        from cmsplugin_blocks.utils.validators import validate_css_classnames
        from cmsplugin_blocks.choices_helpers import get_card_feature_choices

        # Ensure feature classes are valid
        validate_css_classnames([
            item[0] for item in get_card_feature_choices()
        ])

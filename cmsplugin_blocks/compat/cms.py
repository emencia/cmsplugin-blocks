from packaging.version import Version

from django.conf import settings

from cms import __version__
from cms.api import create_page
from cms.utils.urlutils import admin_reverse

DJANGO_CMS4 = Version(__version__) >= Version("4")


class AbstractCmsAPI:
    """
    Abstract to include methods for common operations with DjangoCMS core API.

    It supports both core API from DjangoCMS '3.x' and '4.x'.

    This abstract is suitable to mix within a Unittest class but you will have to set
    attributes ``_author`` and ``_language`` yourself before using methods.

    Attributes:
        _author (User object): User object to use with operation methods that need it.
        _language (string): Language code to use with operation method that need it.
            When undefined it will use the default language from settings.
    """
    def get_author(self):
        if not getattr(self, "_author"):
            raise ValueError(
                "CMS API interface used a method requiring an author but it was not"
                "set. You should set it before."
            )
        return self._author

    def get_language(self, language=None):
        return language or getattr(self, "_language") or settings.LANGUAGE_CODE

    def get_plugin_add_url(self):
        """
        Return the URL to add a new plugin.

        Returns:
            string: The URL.
        """
        return admin_reverse(self._CMS_PLUGIN_ADD_URL_PATTERN)

    def request_plugin_add(self, client, plugin, placeholder, position=1):
        """
        Use a request client to get a plugin creation form.

        .. Note::
            Plugin creation requires more arguments that the edition one because it
            needs to know what kind of plugin and how to create it, edition just
            retrieves this from the plugin instance.

        Returns:
            string: The URL.
        """
        url = self.get_plugin_add_url()
        language = self.get_language()

        if DJANGO_CMS4:
            data = {
                "plugin_type": plugin,
                "placeholder_id": placeholder,
                "cms_path": "/{}/".format(language),
                "plugin_language": language,
                "plugin_position": position,
            }
        else:
            data = {
                "plugin_type": plugin,
                "placeholder_id": placeholder,
                "target_language": language,
                "plugin_language": language,
            }

        return client.get(url, data)

    def get_plugin_edit_url(self, pk=None):
        """
        Return the URL to edit a plugin.

        Seen from requests:
            /admin/cms/placeholder/edit-plugin/1/?cms_path=/admin/cms/placeholder/object/5/edit/1/

        Splitted parts:
            /admin/cms/placeholder/edit-plugin/1/
                ?
                    cms_path=
                        /admin/cms/placeholder/object/5/edit/1/

        Keyword Arguments:
            pk (integer or string): The plugin id. If not given it will be replaced by
                a string placeholder ``{}``. This can be useful to reuse the same blank
                pattern multiple times without repeatedly calling this method.

        Returns:
            string: The URL.
        """
        # '?cms_path=/en/'
        return admin_reverse(self._CMS_PLUGIN_EDIT_URL_PATTERN, args=[pk or "{}"])

    def request_plugin_edit(self, client, pk):
        """
        Use a request client to get a plugin edition form.

        Returns:
            string: The URL.
        """
        url = self.get_plugin_edit_url(pk=pk)

        return client.get(url)

    # For DjangoCMS 4.x
    if DJANGO_CMS4:
        _CMS_PLUGIN_ADD_URL_PATTERN = "cms_placeholder_add_plugin"
        _CMS_PLUGIN_EDIT_URL_PATTERN = "cms_placeholder_edit_plugin"

        def _get_versionning(self, grouper, version_state, language=None):
            from djangocms_versioning.models import Version

            versions = Version.objects.filter_by_grouper(grouper).filter(
                state=version_state
            )
            for version in versions:
                if (
                    hasattr(version.content, "language")
                    and version.content.language == self.get_language(language)
                ):
                    return version

        def publish(self, grouper, language=None):
            from djangocms_versioning.constants import DRAFT

            version = self._get_versionning(grouper, DRAFT, language)
            if version is not None:
                version.publish(self.get_author())

        def unpublish(self, grouper, language=None):
            from djangocms_versioning.constants import PUBLISHED

            version = self._get_versionning(grouper, PUBLISHED, language)
            if version is not None:
                version.unpublish(self.get_author())

        def create_page(self, title, **kwargs):
            kwargs.setdefault("language", self.get_language())
            kwargs.setdefault("created_by", self.get_author())
            kwargs.setdefault("in_navigation", True)
            kwargs.setdefault("limit_visibility_in_menu", None)
            kwargs.setdefault("menu_title", title)
            return create_page(title=title, **kwargs)

        def get_placeholders(self, page):
            return page.get_placeholders(self.get_language())

    # For DjangoCMS 3.x
    else:
        _CMS_PLUGIN_ADD_URL_PATTERN = "cms_page_add_plugin"
        _CMS_PLUGIN_EDIT_URL_PATTERN = "cms_page_edit_plugin"

        def publish(self, page, language=None):
            page.publish(language)

        def unpublish(self, page, language=None):
            page.unpublish(language)

        def create_page(self, title, **kwargs):
            kwargs.setdefault("language", self.get_language())
            kwargs.setdefault("menu_title", title)
            return create_page(title=title, **kwargs)

        def get_placeholders(self, page):
            return page.get_placeholders()


class CmsAPI(AbstractCmsAPI):
    """
    DjangoCMS core API interface for common operations.

    Arguments:
        author (User object): User object to use with operation methods that need it.
        language (string): Language code to use with operation method that need it.
            When undefined it will use the default language from settings.
    """
    def __init__(self, language=None, author=None):
        self._author = author
        self._language = language

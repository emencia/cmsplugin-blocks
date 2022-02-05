"""
Test utilities
"""
import os

import pytest
import factory
import faker

from django.test.html import HTMLParseError, parse_html

from cms.api import add_plugin
from cms.models import Placeholder
from cms.test_utils.testcases import CMSTestCase
from cmsplugin_blocks.utils.factories import create_image_file


def get_fake_words(length=1):
    """
    Shortand to build a string of fake words depending given required count of
    words.
    """
    Faker = faker.Faker()
    words = Faker.words(nb=length)

    return " ".join(words)


def get_test_source(storage, *args, **kwargs):
    """
    Shortcut helper to create a dummy image, save it to the FS and get its
    final path from storage.

    Arguments:
        storage (django.core.files.storage.Storage): Storage class to use to
            save file to the file system.

    Keyword Arguments:
        storage (django.core.files.storage.Storage): Storage class to use to
            save file to the file system. This is a required argument.
        destination_dir (string): relative directory path where to save file
            in storage directory. Default to "pil".
        *args: Any other positionnal arguments are passed to
            ``create_image_file``.
        **kwargs: Any other Keyword arguments are passed to
            ``create_image_file``.

    Returns:
        django.core.files.File: File object with the right final file path.
    """
    destination_dir = kwargs.pop("destination_dir", "pil")

    image = create_image_file(*args, **kwargs)

    destination = os.path.join(destination_dir, image.name)
    source_filepath = storage.save(destination, image)

    # Trick to update name to final destination since File object is not
    # automatically updated to the final filepath during storage.
    image.name = source_filepath

    return image


def assert_and_parse_html(html):
    """
    Shortand to use Django HTML parsing as object to use in assert
    """
    dom = parse_html(html)
    return dom


class FixturesTestCaseMixin(object):
    """
    Mixin to inject pytest fixtures on testcase.

    These fixtures will be available for every testcase tests.
    """

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, testsettings):
        self._caplog = caplog
        self._testsettings = testsettings


class CMSPluginTestCase(CMSTestCase):
    """
    Enriched CMS test case object to include useful stuff about plugin
    rendering.

    NOTE:
        The CMSTestCase mixin from DjangoCMS is making queries in its "tearDown"
        method which causes database transaction errors with tests that have
        already generated a database error.

        A workaround is to decorate such tests with
        ``django.db.transaction`` (or to use it as a context manager) so that
        the test has its own transaction that is rolled back before the TearDown
        method sends its queries to the database.
    """

    def get_practical_plugin_context(self, extra_context=None):
        """
        Build a template context with dummy request object and
        instanciated content renderer suitable to perform full rendering of
        any plugin.

        NOTE:
            CMSTestCase use a dummy AnonymousUser on default behavior, you can
            override it with a custom user as an ``user`` attribute on your
            test case object. In most cases we should in fact define this
            attribute during test to use a UserFactory instead of a global
            user for every tests.

        Keyword Arguments:
            extra_context (dict): Dictionnary to add extra variable to context.
                Default to an empty dict.

        Returns:
            django.template.Context: Template context filled with request
            object as ``request`` item and content renderer as
            ``cms_content_renderer`` item.
        """
        context = self.get_context()
        if extra_context:
            context.update(extra_context)

        renderer = self.get_content_renderer(request=context["request"])

        # 'cms_content_renderer' is the attempted item name from CMS rendering
        # machinery
        context["cms_content_renderer"] = renderer

        return context

    def create_basic_render(self, plugin, slot_name="test", lang="en",
                            copy_relations_from=None, **kwargs):
        """
        A shortcut to create a basic render for a plugin
        """
        # Create a dummy slot if not given in arguments
        placeholder = (kwargs.pop("placeholder", None)
                       or Placeholder.objects.create(slot=slot_name))

        # Template context
        context = self.get_practical_plugin_context()


        # Init plugin with some content
        model_instance = add_plugin(
            placeholder,
            plugin,
            lang,
            **kwargs
        )

        # Copy relation when asked, this is required for plugin model with
        # foreign key since djangocms machinery does not perform it with API
        if copy_relations_from and hasattr(model_instance, "copy_relations"):
            model_instance.copy_relations(copy_relations_from)

        # Render placeholder so plugin is fully rendered in real situation
        html = context["cms_content_renderer"].render_placeholder(
            placeholder, context=context, language=lang
        )

        return placeholder, model_instance, context, html

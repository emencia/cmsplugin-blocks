"""
Some various utilities to ease making tests around Django and HTML responses.

"""
import os
import hashlib

from django.contrib.sites.models import Site
from django.template.response import TemplateResponse
from django.test.html import parse_html
from django.urls import reverse

from pyquery import PyQuery as pq

from .factories import create_image_file


# A dummy password that should pass form validation
VALID_PASSWORD_SAMPLE = "Azerty12345678"


# A dummy blank GIF file in byte value to simulate an uploaded file like with
# 'django.core.files.uploadedfile.SimpleUploadedFile'
DUMMY_GIF_BYTES = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)


def get_website_url(site_settings=None):
    """
    A shortand to retrieve the full website URL according to Site ID and HTTP
    protocole settings.

    Keyword Arguments:
        site_settings (django.conf.settings): Settings object, if not given the method
            will be unable to determine if HTTPS is enabled or not, so it will always
            return a HTTP URL.

    Returns:
        string: Full website URL.
    """
    domain = Site.objects.get_current().domain

    protocol = "http://"
    if site_settings and site_settings.HTTPS_ENABLED:
        protocol = "https://"

    return "{}{}".format(protocol, domain)


def get_relative_path(site_url, url):
    """
    From given URL, retrieve the relative path (URL without domain and starting
    slash).

    Arguments:
        site_url (string): Website URL to remove from given ``url``
            argument.
        url (string): Full URL (starting with http/https) to make relative to
            website URL.

    Returns:
        string: Admin change view URL path for given model object.
    """
    if url.startswith(site_url):
        return url[len(site_url):]

    return url


def get_admin_add_url(model):
    """
    Return the right admin URL for add form view for given class.

    Arguments:
        model (Model object): A model object to use to find its admin
            add form view URL.

    Returns:
        string: Admin add form view URL path.
    """
    url_pattern = "admin:{app}_{model}_add"

    return reverse(url_pattern.format(
        app=model._meta.app_label,
        model=model._meta.model_name
    ))


def get_admin_change_url(obj):
    """
    Return the right admin URL for a change view for given object.

    Arguments:
        obj (Model object): A model object instance to use to find its admin
            change view URL.

    Returns:
        string: Admin change view URL path.
    """
    url_pattern = "admin:{app}_{model}_change"

    return reverse(url_pattern.format(
        app=obj._meta.app_label,
        model=obj._meta.model_name
    ), args=[
        obj.pk
    ])


def get_admin_list_url(model):
    """
    Return the right admin URL for a list view for given class.

    Arguments:
        model (Model object): A model object to use to find its admin
            list view URL.

    Returns:
        string: Admin list view URL path.
    """
    url_pattern = "admin:{app}_{model}_changelist"

    return reverse(url_pattern.format(
        app=model._meta.app_label,
        model=model._meta.model_name
    ))


def decode_response_or_string(content):
    """
    Shortand to get HTML string from either a TemplateResponse (as returned
    from Django test client) or a simple string so you can blindly give a
    response or a string without to care about content type.

    Arguments:
        content (TemplateResponse or string): If content is a string it will
            just return it. If content is a TemplateResponse it will decode byte
            string from its ``content`` attribute.

    Returns:
        string: HTML string.
    """
    if isinstance(content, TemplateResponse):
        return content.content.decode()
    return content


def html_element(content):
    """
    Shortand to use Django HTML parsing on given content.

    This is more useful for comparaison on HTML parts.

    Arguments:
        content (TemplateResponse or string): HTML content to parse.

    Returns:
        django.test.html.Element: A Python object structure able to perform
        comparaison on a semantical way. See ``django.test.html.parse_html`` for
        more details.
    """
    return parse_html(
        decode_response_or_string(content)
    )


def html_pyquery(content):
    """
    Shortand to use Pyquery parsing on given content.

    This is more useful to dig in advanced HTML content. PyQuery is basically a
    wrapper around ``lxml.etree`` it helps with a more intuitive API (alike
    Jquery) to traverse elements but when reaching a node content it will
    return ``lxml.html.HtmlElement`` object which have a less intuitive API.

    Arguments:
        content (TemplateResponse or string): HTML content to parse.

    Returns:
        pyquery.PyQuery: A PyQuery object.
    """
    return pq(
        decode_response_or_string(content),
        parser='html'
    )


def compact_form_errors(form):
    """
    Build a compact dict of field errors without messages.

    This is a helper for errors, keeping it more easy to test since messages
    may be too long and can be translated which is more difficult to test.

    Arguments:
        form (django.forms.Form): A bounded form.

    Returns:
        dict: A dict of invalid fields, each item is indexed by field name and
        value is a list of error codes.
    """
    errors = {}

    for name, validationerror in form.errors.as_data().items():
        errors[name] = [item.code for item in validationerror]

    return errors


def sum_file_object(fileobj):
    """
    Return a hash checksum for given file object using "Black2b" algorithm.

    Arguments:
        fileobj (object): Any file valid object with ``getvalue`` or ``read`` method.

    Returns:
        string: Checksum for file object.
    """
    algorithm = hashlib.blake2b()

    # Some file object alike like BytesIO does not return correct content from "read()"
    # method
    if hasattr(fileobj, "getvalue"):
        content = fileobj.getvalue()
    else:
        content = fileobj.read()

    algorithm.update(content)

    return algorithm.hexdigest()


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

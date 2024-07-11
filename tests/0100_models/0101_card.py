from cmsplugin_blocks.models.card import Card
from cmsplugin_blocks.utils.factories import get_fake_words


def test_basic(db, settings):
    """
    Basic model saving with required fields should not fail
    """
    instance = Card(
        content="Foo",
        template="cmsplugin_blocks/card/test.html",
    )
    instance.full_clean()
    instance.save()

    created = Card.objects.get(pk=instance.id)

    assert 1 == Card.objects.filter(content="Foo").count()
    assert "Foo" == created.content


def test_str_truncation_under_limit(db, settings):
    """
    Model str should be equal to save string when under the limit.
    """
    content = get_fake_words(length=settings.BLOCKS_MODEL_TRUNCATION_LENGTH)
    instance = Card(
        content=content,
        template="cmsplugin_blocks/card/test.html"
    )
    instance.full_clean()
    instance.save()

    assert content == str(instance)


def test_str_truncation_over_limit(db, settings):
    """
    Model str should be truncated to X words when over the limit from setting
    ``BLOCKS_MODEL_TRUNCATION_LENGTH``.
    """
    content = get_fake_words(length=(settings.BLOCKS_MODEL_TRUNCATION_LENGTH + 3))
    instance = Card(
        content=content,
        template="cmsplugin_blocks/card/test.html"
    )
    instance.full_clean()
    instance.save()

    assert len(content) > len(str(instance))
    assert str(instance).endswith(settings.BLOCKS_MODEL_TRUNCATION_CHR)


def test_str_strip_tags(db, settings):
    """
    Model str should be cleaned from any HTML tags and unicode character are
    not broken.
    """
    instance = Card(
        content="<p>Foo 日本</p>",
        template="cmsplugin_blocks/card/test.html"
    )
    instance.save()

    assert "<p>Foo 日本</p>" == instance.content
    assert "Foo 日本" == str(instance)


def test_image_format(db, settings):
    """
    Method to get image format should return a valid value without any error.
    """
    instance = Card(image="foo.jpg")
    instance.full_clean()
    instance.save()

    assert instance.get_image_format() == "JPEG"

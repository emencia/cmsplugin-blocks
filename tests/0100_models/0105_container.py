from cmsplugin_blocks.models.container import Container
from cmsplugin_blocks.utils.factories import get_fake_words


def test_basic(db, settings):
    """
    Basic model saving with required fields should not fail
    """
    instance = Container(
        content="Foo",
        template="Dummy",
        features=["foo"],
    )
    instance.save()

    created = Container.objects.get(pk=instance.id)

    assert 1 == Container.objects.filter(content="Foo").count()
    assert "Foo" == created.content
    assert ["foo"] == created.features


def test_features_multiple(db, settings):
    """
    Demonstrate how to add multiple feature items
    """
    instance = Container(
        content="Foo",
        template="Dummy",
        features=["foo", "bar"],
    )
    instance.save()

    created = Container.objects.get(pk=instance.id)

    assert ["foo", "bar"] == created.features


def test_features_wrong(db, settings):
    """
    Demonstrate that giving a string to feature does not work as it could be expected.
    """
    instance = Container(
        content="Foo",
        template="Dummy",
        features="foo",
    )
    instance.save()

    created = Container.objects.get(pk=instance.id)

    assert ["f", "o", "o"] == created.features


def test_str_truncation_under_limit(db, settings):
    """
    Model str should be equal to save string when under the limit.
    """
    content = get_fake_words(length=settings.BLOCKS_MODEL_TRUNCATION_LENGTH)
    instance = Container(
        content=content,
        template="Dummy"
    )
    instance.save()

    assert content == str(instance)


def test_str_truncation_over_limit(db, settings):
    """
    Model str should be truncated to X words when over the limit from setting
    ``BLOCKS_MODEL_TRUNCATION_LENGTH``.
    """
    content = get_fake_words(length=(settings.BLOCKS_MODEL_TRUNCATION_LENGTH + 3))
    instance = Container(
        content=content,
        template="Dummy"
    )
    instance.save()

    assert len(content) > len(str(instance))
    assert str(instance).endswith(settings.BLOCKS_MODEL_TRUNCATION_CHR)


def test_str_strip_tags(db, settings):
    """
    Model str should be cleaned from any HTML tags and unicode character are
    not broken.
    """
    instance = Container(
        content="<p>Foo 日本</p>",
        template="Dummy"
    )
    instance.save()

    assert "<p>Foo 日本</p>" == instance.content
    assert "Foo 日本" == str(instance)


def test_image_format(db, settings):
    """
    Method to get image format should return a valid value without any error.
    """
    instance = Container(image="foo.jpg")
    instance.save()

    assert instance.get_image_format() == "JPEG"

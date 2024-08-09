from cmsplugin_blocks.models.accordion import Accordion, AccordionItem
from cmsplugin_blocks.utils.factories import get_fake_words


def test_basic(db, settings):
    """
    Basic model saving with required fields should not fail
    """
    accordion = Accordion(
        title="Foo",
        template="Dummy"
    )
    accordion.save()

    assert 1 == Accordion.objects.filter(title="Foo").count()
    assert "Foo" == accordion.title

    item = AccordionItem(
        accordion=accordion,
        order=42,
        image="ping.jpg",
    )
    item.save()

    assert 1 == AccordionItem.objects.filter(image="ping.jpg").count()
    assert 42 == item.order
    assert accordion == item.accordion
    assert [item] == list(accordion.accordion_item.all())


def test_str_truncation_under_limit(db, settings):
    """
    Model str should be equal to saved string when under the limit.
    """
    title = get_fake_words(length=settings.BLOCKS_MODEL_TRUNCATION_LENGTH)
    accordion = Accordion(
        title=title,
        template="Dummy"
    )
    accordion.save()

    assert title == str(accordion)

    title = get_fake_words(length=settings.BLOCKS_MODEL_TRUNCATION_LENGTH)
    item = AccordionItem(
        accordion=accordion,
        title=title,
        order=42,
        image="ping.jpg",
    )
    item.save()

    assert title == str(item)


def test_str_truncation_over_limit(db, settings):
    """
    Model str should be truncated to X words when over the limit from setting
    ``BLOCKS_MODEL_TRUNCATION_LENGTH``.
    """
    limit = settings.BLOCKS_MODEL_TRUNCATION_LENGTH + 3

    title = get_fake_words(length=limit)
    accordion = Accordion(
        title=title,
        template="Dummy"
    )
    accordion.save()

    assert len(title) > len(str(accordion))
    assert str(accordion).endswith(settings.BLOCKS_MODEL_TRUNCATION_CHR)

    title = get_fake_words(length=limit)
    item = AccordionItem(
        accordion=accordion,
        title=title,
        order=42,
        image="ping.jpg",
    )
    item.save()

    assert len(title) > len(str(item))
    assert str(item).endswith(settings.BLOCKS_MODEL_TRUNCATION_CHR)


def test_str_strip_tags(db, settings):
    """
    Model str should be cleaned from any HTML tags and unicode character are
    not broken.
    """
    accordion = Accordion(
        title="<p>Foo 日本</p>",
        template="Dummy"
    )
    accordion.save()

    assert "<p>Foo 日本</p>" == accordion.title
    assert "Foo 日本" == str(accordion)

    item = AccordionItem(
        accordion=accordion,
        title="<p>Ping 日本</p>",
        order=42,
        image="ping.jpg",
    )
    item.save()

    assert "<p>Ping 日本</p>" == item.title
    assert "Ping 日本" == str(item)


def test_item_image_format(db, settings):
    """
    Method to get image format should return a valid value without any error.
    """
    accordion = Accordion(
        title="Foo",
        template="Dummy"
    )
    accordion.save()

    item = AccordionItem(
        accordion=accordion,
        order=42,
        image="foo.jpg",
    )
    item.save()

    assert item.get_image_format() == "JPEG"

import pytest

from django.conf import settings

from tests.utils import get_fake_words

from cmsplugin_blocks.models.slider import Slider, SlideItem


def test_basic(db, settings):
    """
    Basic model saving with required fields should not fail
    """
    slider = Slider(
        title="Foo",
        template="Dummy"
    )
    slider.save()

    assert 1 == Slider.objects.filter(title="Foo").count()
    assert "Foo" == slider.title

    item = SlideItem(
        slider=slider,
        order=42,
        image="ping.jpg",
    )
    item.save()

    assert 1 == SlideItem.objects.filter(image="ping.jpg").count()
    assert 42 == item.order
    assert slider == item.slider
    assert [item] == list(slider.slide_item.all())


def test_str_truncation_under_limit(db, settings):
    """
    Model str should be equal to saved string when under the limit.
    """
    title = get_fake_words(length=settings.BLOCKS_MODEL_TRUNCATION_LENGTH)
    slider = Slider(
        title=title,
        template="Dummy"
    )
    slider.save()

    assert title == str(slider)

    title = get_fake_words(length=settings.BLOCKS_MODEL_TRUNCATION_LENGTH)
    item = SlideItem(
        slider=slider,
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
    slider = Slider(
        title=title,
        template="Dummy"
    )
    slider.save()

    assert len(title) > len(str(slider))
    assert str(slider).endswith(settings.BLOCKS_MODEL_TRUNCATION_CHR)

    title = get_fake_words(length=limit)
    item = SlideItem(
        slider=slider,
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
    slider = Slider(
        title="<p>Foo 日本</p>",
        template="Dummy"
    )
    slider.save()

    assert "<p>Foo 日本</p>" == slider.title
    assert "Foo 日本" == str(slider)

    item = SlideItem(
        slider=slider,
        title="<p>Ping 日本</p>",
        order=42,
        image="ping.jpg",
    )
    item.save()

    assert "<p>Ping 日本</p>" == item.title
    assert "Ping 日本" == str(item)

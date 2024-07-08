from cmsplugin_blocks.choices_helpers import get_container_template_default
from cmsplugin_blocks.factories import ContainerFactory


def test_factory(db):
    """
    Factory should correctly create a new object without any errors
    """
    instance = ContainerFactory()
    assert instance.template == get_container_template_default()

    instance = ContainerFactory(template="foo")
    assert instance.template == "foo"

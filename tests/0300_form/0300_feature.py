import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from cmsplugin_blocks.forms import FeatureImportForm
from cmsplugin_blocks.models import Feature
from cmsplugin_blocks.utils.tests import flatten_form_errors


def test_import_empty(db):
    """
    Form should not be valid with missing required fields.
    """
    form = FeatureImportForm({})

    assert form.is_valid() is False
    assert "json_file" in form.errors
    assert len(form.errors) == 1


@pytest.mark.parametrize("dump, expected", [
    (
        "invalid.json",
        ["File is not valid JSON: Expecting value: line 1 column 1 (char 0)"],
    ),
    (
        "not_a_dict.json",
        ["JSON should be a dictionnary not a: list"],
    ),
    (
        "missing_items.json",
        ["JSON is missing 'items' item for the feature data"],
    ),
    (
        "items_not_a_list.json",
        ["Item 'items' must be a list"],
    ),
    (
        "some_items_errors.json",
        [
            "Some dump items are invalid:",
            "#2 is missing one or more required items",
            "#3 is missing one or more required items",
            "#4 is missing one or more required items"
        ],
    ),
    (
        "not_unique.json",
        [
            "Some dump items are invalid:",
            "#2 define a title that already exists"
        ],
    ),
    (
        "invalid_scopes.json",
        [
            "Some dump items are invalid:",
            "#1 define a scope choice that is not enabled"
        ],
    ),
    (
        "invalid_plugins.json",
        [
            "Some dump items are invalid:",
            "#2 define a plugin name that is not enabled",
            "#3 define a plugin name that is not enabled"
        ],
    ),
])
def test_import_dump_validation_errors(db, settings, tests_settings, dump, expected):
    """
    Form should validate JSON to not let pass any invalid content.
    """
    settings.LANGUAGE_CODE = "en"

    filepath = tests_settings.fixtures_path / "feature_samples" / dump

    dump = SimpleUploadedFile(
        "dump.json",
        filepath.read_bytes(),
        content_type="application/json"
    )

    form = FeatureImportForm({}, {"json_file": dump})
    is_valid = form.is_valid()
    assert is_valid is False

    errors = flatten_form_errors(form)
    print()
    print(errors)
    print()
    assert errors == {"json_file": expected}


def test_import_dump_save(db, tests_settings):
    """
    Form should properly save elligible dump items and return stats about processed
    items.
    """
    filepath = tests_settings.fixtures_path / "feature_samples" / "valid.json"

    dump = SimpleUploadedFile(
        "dump.json",
        filepath.read_bytes(),
        content_type="application/json"
    )

    form = FeatureImportForm({}, {"json_file": dump})
    is_valid = form.is_valid()
    assert is_valid is True

    # Without commit, dump is fully processed but nothing is saved, stats still are
    # correct
    results = form.save(commit=False)
    assert len(results["created"]) == 7
    assert len(results["duplicates"]) == 0
    assert results["disallowed_scopes"] == []
    assert len(results["ignored"]) == 0
    assert Feature.objects.count() == 0

    # With commit, dump items are saved, stats are identical
    results = form.save(commit=True)
    assert len(results["created"]) == 7
    assert len(results["duplicates"]) == 0
    assert results["disallowed_scopes"] == []
    assert len(results["ignored"]) == 0
    assert Feature.objects.count() == 7

    # With commit and the same entries nothing is saved, instead everything is marked
    # as duplicate
    results = form.save(commit=True)
    assert len(results["created"]) == 0
    assert len(results["duplicates"]) == 7
    assert results["disallowed_scopes"] == []
    assert len(results["ignored"]) == 0
    assert Feature.objects.count() == 7


def test_import_dump_scoped_save(db, tests_settings):
    """
    When scopes are selected, they should be ignored from form save.
    """
    filepath = tests_settings.fixtures_path / "feature_samples" / "valid.json"

    dump = SimpleUploadedFile(
        "dump.json",
        filepath.read_bytes(),
        content_type="application/json"
    )

    form = FeatureImportForm({"scopes": ["color"]}, {"json_file": dump})
    assert form.is_valid() is True
    results = form.save(commit=False)
    assert len(results["created"]) == 5
    assert results["disallowed_scopes"] == ["color"]
    assert len(results["ignored"]) == 2

    form = FeatureImportForm({"scopes": ["size", "color"]}, {"json_file": dump})
    assert form.is_valid() is True
    results = form.save(commit=False)
    assert len(results["created"]) == 2
    assert results["disallowed_scopes"] == ["size", "color"]
    assert len(results["ignored"]) == 5


def test_import_dump_value_whitespaces(db, settings, tests_settings):
    """
    Importation should properly manage whitespace validation in Feature 'value' field
    depending from setting 'BLOCKS_FEATURE_ALLOW_MULTIPLE_CLASSES'.
    """
    settings.LANGUAGE_CODE = "en"

    filepath = tests_settings.fixtures_path / "feature_samples" / "whitespaces.json"
    dump = SimpleUploadedFile(
        "dump.json",
        filepath.read_bytes(),
        content_type="application/json"
    )

    # When whitespace are not allowed, the dump will fail on errors
    settings.BLOCKS_FEATURE_ALLOW_MULTIPLE_CLASSES = False
    form = FeatureImportForm({}, {"json_file": dump})
    is_valid = form.is_valid()
    assert is_valid is False
    errors = flatten_form_errors(form)
    assert errors == {"json_file": [
        "Some dump items are invalid:",
        "#1 has invalid CSS classname(s)"
    ]}

    # When whitespace is allowed, the dump will succeed
    settings.BLOCKS_FEATURE_ALLOW_MULTIPLE_CLASSES = True
    form = FeatureImportForm({}, {"json_file": dump})
    is_valid = form.is_valid()
    assert is_valid is True
    results = form.save(commit=False)
    assert len(results["created"]) == 2
    assert len(results["duplicates"]) == 0
    assert results["disallowed_scopes"] == []
    assert len(results["ignored"]) == 0
    assert Feature.objects.count() == 0

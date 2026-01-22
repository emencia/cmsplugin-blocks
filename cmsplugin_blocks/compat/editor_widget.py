"""
We support multiple editor widget in this order:

* djangocms-text;
* djangocms-text-ckeditor;
* Django Textarea;

Where the first one to be installed is used else we fallback on the builtin Django
widget.
"""
try:
    import djangocms_text  # noqa: F401,F403
except ImportError:
    try:
        import djangocms_text_ckeditor  # noqa: F401,F403
    except ImportError:
        from django.forms import Textarea as TextEditorWidget  # noqa: F401,F403
    else:
        from djangocms_text_ckeditor.widgets import TextEditorWidget  # noqa: F401,F403
else:
    from djangocms_text.widgets import TextEditorWidget  # noqa: F401,F403

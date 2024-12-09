"""
We support multiple editor widget in this order:

* djangocms-text;
* djangocms-text-ckeditor;
* Django Textarea;

Where the first one to be installed is used else we fallback on the builtin Django
widget.
"""
try:
    import djangocms_text
except ImportError:
    try:
        import djangocms_text_ckeditor
    except ImportError:
        from django.forms import Textarea as TextEditorWidget
    else:
        from djangocms_text.widgets import TextEditorWidget
else:
    from djangocms_text.widgets import TextEditorWidget

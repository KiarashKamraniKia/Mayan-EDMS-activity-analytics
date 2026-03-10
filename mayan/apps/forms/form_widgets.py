from django.forms.widgets import *  # NOQA
from django.forms.widgets import __all__ as django_forms_widgets_all
from django.forms.widgets import Widget

__all__ = django_forms_widgets_all + ('DropzoneWidget',)


class DropzoneWidget(Widget):
    template_name = 'forms/forms/widgets/dropzone.html'

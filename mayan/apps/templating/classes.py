import functools
import hashlib
import re

from django.template.response import TemplateResponse
from django.template.utils import EngineHandler
from django.urls import reverse

from .literals import REGULAR_AJAX_TEMPLATE_HASH_EXCLUDE_PAIR

REGEX_COMPILED_AJAX_TEMPLATE_HASH_EXCLUDE = re.compile(
    pattern=REGULAR_AJAX_TEMPLATE_HASH_EXCLUDE_PAIR, flags=re.DOTALL
)


class AJAXTemplate:
    _registry = {}

    @classmethod
    def all(cls, rendered=False, request=None):
        if not rendered:
            return cls._registry.values()
        else:
            result = []
            for template in cls._registry.values():
                result.append(
                    template.render(request=request)
                )
            return result

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    def __init__(self, name, template_name, context=None):
        self.context = context or None
        self.name = name
        self.template_name = template_name
        self.__class__._registry[name] = self

    def get_absolute_url(self):
        return reverse(
            kwargs={'name': self.name}, viewname='rest_api:template-detail'
        )

    def render(self, request):
        template = TemplateResponse(
            context=self.context, request=request,
            template=self.template_name
        )
        result = template.render()

        self.html = result.rendered_content.replace('\n', '')

        hash_string_raw = result.content.decode()
        hash_string_cleaned = REGEX_COMPILED_AJAX_TEMPLATE_HASH_EXCLUDE.sub(
            repl='', string=hash_string_raw
        )
        hash_string_final = hash_string_cleaned.encode()
        hash_object = hashlib.sha256(string=hash_string_final)
        self.hex_hash = hash_object.hexdigest()

        return self


class Template:
    @classmethod
    @functools.cache
    def get_backend(cls):
        engine_handler = EngineHandler(
            templates=(
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'OPTIONS': {
                        'builtins': [
                            'mathfilters.templatetags.mathfilters',
                            'mayan.apps.templating.templatetags.templating_datetime_tags',
                            'mayan.apps.templating.templatetags.templating_regex_tags',
                            'mayan.apps.templating.templatetags.templating_tags'
                        ]
                    }
                },
            )
        )
        return engine_handler['django']

    def __init__(self, template_string):
        self._template = Template.get_backend().from_string(
            template_code=template_string
        )

    def render(self, context=None):
        if context is None:
            context = {}

        return self._template.render(context=context)

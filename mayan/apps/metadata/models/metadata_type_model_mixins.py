from django.core.exceptions import ValidationError
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from mayan.apps.common.serialization import yaml_load
from mayan.apps.common.utils import comma_splitter
from mayan.apps.templating.classes import Template

from ..classes import MetadataLookup

from ..classes import MetadataParser, MetadataValidator


class MetadataTypeBusinessLogicMixin:
    def get_default_value(self):
        template = Template(template_string=self.default)
        return template.render()

    def get_lookup_values(self):
        template = Template(template_string=self.lookup)

        template_result = template.render(
            context=MetadataLookup.get_as_context()
        )

        return comma_splitter(string=template_result)

    def get_parser_class(self):
        if self.parser not in MetadataParser.get_all():
            raise ValidationError(
                message=_(
                    message='Invalid parser `%s`'
                ) % self.parser
            )

        parser_class = import_string(dotted_path=self.parser)

        return parser_class

    def get_parser_instance(self):
        parser_class = self.get_parser_class()
        stream = self.parser_arguments or '{}'
        parser_arguments = yaml_load(stream=stream)
        parser = parser_class(**parser_arguments)
        return parser

    def get_required_for(self, document_type):
        """
        Determine if the metadata type is required for the specified document
        type.
        """
        queryset = document_type.metadata.filter(
            required=True, metadata_type=self
        )

        return queryset.exists()

    def get_validator_class(self):
        if self.validation not in MetadataValidator.get_all():
            raise ValidationError(
                message=_(
                    message='Invalid validator `%s`'
                ) % self.validation
            )

        validator_class = import_string(dotted_path=self.validation)

        return validator_class

    def get_validator_instance(self):
        validator_class = self.get_validator_class()
        stream = self.validation_arguments or '{}'
        validator_arguments = yaml_load(stream=stream)
        validator = validator_class(**validator_arguments)

        return validator

from django.utils.module_loading import import_string

from mayan.apps.common.serialization import yaml_load
from mayan.apps.common.utils import comma_splitter
from mayan.apps.templating.template_backends import Template


class MetadataTypeBusinessLogicMixin:
    def get_default_value(self):
        template = Template(template_string=self.default)
        return template.render()

    def get_lookup_values(self):
        template = Template(
            context_entry_name_list=('groups', 'users'),
            template_string=self.lookup
        )

        template_result = template.render()

        return comma_splitter(string=template_result)

    def get_parser_class(self):
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
        validator_class = import_string(dotted_path=self.validation)

        return validator_class

    def get_validator_instance(self):
        validator_class = self.get_validator_class()
        stream = self.validation_arguments or '{}'
        validator_arguments = yaml_load(stream=stream)
        validator = validator_class(**validator_arguments)

        return validator

import hashlib

from django.core import serializers

from mayan.apps.common.serialization import yaml_load


class WorkflowTransitionFieldBusinessLogicMixin:
    def get_hash(self):
        string = serializers.serialize(
            format='json', queryset=(self,)
        ).encode()
        hash_object = hashlib.sha256(string=string)
        return hash_object.hexdigest()

    def get_widget_kwargs(self):
        stream = self.widget_kwargs or '{}'
        return yaml_load(stream=stream)

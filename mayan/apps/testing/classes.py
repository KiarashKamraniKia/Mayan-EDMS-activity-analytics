from django.apps import apps

from mayan.apps.common.class_mixins import AppsModuleLoaderMixin


class TestWorkerInitializationContext:
    def __init__(
        self, path_media_root_old, path_media_root_new, worker_id
    ):
        self.path_media_root_old = path_media_root_old
        self.path_media_root_new = path_media_root_new
        self.worker_id = worker_id


class TestWorkerInitialization(AppsModuleLoaderMixin):
    _callback_list = []
    _loader_module_name = 'tests.parallel'

    @classmethod
    def do_initialize(cls, context):
        for callback in cls._callback_list:
            callback(context=context)

    @classmethod
    def get_loader_app_configs(cls):
        # Only Mayan apps register worker initialization callbacks.
        return [
            app for app in apps.get_app_configs()
            if app.name.startswith('mayan.apps.')
        ]

    @classmethod
    def register(cls, callback):
        cls._callback_list.append(callback)

from importlib import import_module
import logging

from django.apps import apps

logger = logging.getLogger(name=__name__)


class AppsModuleLoaderMixin:
    # __loader_module_sets is used to avoid double imports, it should not
    # be modified by the user.
    __loader_module_sets = {}

    # _loader_module_name must be set to the module name that is to be
    # uploaded by the class mixin.
    _loader_module_name = None

    @classmethod
    def get_loader_app_configs(cls):
        return apps.get_app_configs()

    @classmethod
    def load_modules(cls):
        # This set keeps track of what apps have already been processed.
        cls.__loader_module_sets.setdefault(
            cls._loader_module_name, set()
        )

        for app in cls.get_loader_app_configs():
            if app not in cls.__loader_module_sets[cls._loader_module_name]:
                try:
                    import_module(
                        name='{}.{}'.format(
                            app.name, cls._loader_module_name
                        )
                    )
                except ImportError as exception:
                    # Determine which errors during import should be ignored
                    # and which are serious enough to raise.
                    full_module_name = '{}.{}'.format(
                        app.name, cls._loader_module_name
                    )
                    missing_module_name = getattr(exception, 'name', None)
                    missing_module_name_string = '{}.'.format(missing_module_name)

                    app_lacks_module = False
                    if isinstance(exception, ModuleNotFoundError) and missing_module_name:
                        app_lacks_module = (
                            full_module_name == missing_module_name
                        ) or full_module_name.startswith(missing_module_name_string)

                    if not app_lacks_module:
                        raise

                finally:
                    cls.__loader_module_sets[
                        cls._loader_module_name
                    ].add(app)

        cls.post_load_modules()

    @classmethod
    def post_load_modules(cls):
        """
        Optional method that will get executed when the method `load_modules`
        completes.
        """

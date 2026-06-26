from pathlib import Path

from mayan.apps.testing.classes import TestWorkerInitialization

from ..classes import DefinedStorage


def test_worker_initialization_storage(context):
    for defined_storage in DefinedStorage._registry.values():
        kwargs = defined_storage.kwargs
        if isinstance(kwargs, dict):
            location = kwargs.get('location')
            if isinstance(location, str):
                path_location = Path(location)
                if path_location.is_relative_to(context.path_media_root_old):
                    path_location_new = context.path_media_root_new / path_location.relative_to(
                        context.path_media_root_old
                    )
                    kwargs['location'] = str(path_location_new)


TestWorkerInitialization.register(callback=test_worker_initialization_storage)

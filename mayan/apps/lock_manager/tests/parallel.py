from mayan.apps.storage.settings import setting_temporary_directory
from mayan.apps.testing.classes import TestWorkerInitialization

from ..backends.base import LockingBackend


def test_worker_initialization_lock_manager(context):
    path_temporary = context.path_media_root_new / 'temporary'
    path_temporary.mkdir(exist_ok=True, parents=True)

    setting_temporary_directory.do_value_override(
        value=str(path_temporary)
    )

    locking_backend = LockingBackend.get_backend()
    locking_backend._is_initialized = False
    lock = locking_backend.acquire_lock(
        name='mayan_test_worker_initialization'
    )
    lock.release()


TestWorkerInitialization.register(
    callback=test_worker_initialization_lock_manager
)

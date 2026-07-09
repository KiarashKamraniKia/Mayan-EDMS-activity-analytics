from ...tasks import (
    task_deindex_instance, task_index_instances, task_reindex_backend
)

from .base import SearchTestMixin


class SearchTaskTestMixin(SearchTestMixin):
    def _execute_task_deindex_instance(self):
        app_label = self._test_object._meta.app_label
        model_name = self._test_object._meta.model_name
        object_id = self._test_object.pk

        task = task_deindex_instance.apply_async(
            kwargs={
                'app_label': app_label, 'model_name': model_name,
                'object_id': object_id
            }
        )
        task.get()

    def _execute_task_index_instances(self):
        task = task_index_instances.apply_async(
            kwargs={
                'id_list': (self._test_object.pk,),
                'search_model_full_name': self._test_model_search.full_name
            }
        )
        task.get()

    def _execute_task_reindex_backend(self):
        task = task_reindex_backend.apply_async()
        task.get()

from ..classes import PythonDependency

from .literals import (
    TEST_DEPENDENCY_GROUP_NAME, TEST_DEPENDENCY_GROUP_ENTRY_NAME
)


class CheckVersionViewTestMixin:
    def _request_check_version_view(self):
        return self.get(viewname='dependencies:check_version_view')


class DependencyGroupEntryDetailViewTestMixin:
    def request_test_dependency_group_entry_detail_view(self):
        return self.get(
            viewname='dependencies:dependency_group_entry_detail', kwargs={
                'dependency_group_name': TEST_DEPENDENCY_GROUP_NAME,
                'dependency_group_entry_name': TEST_DEPENDENCY_GROUP_ENTRY_NAME
            }
        )


class PythonDependencyTestMixin:
    def setUp(self):
        super().setUp()
        self.mock_path_list = self._get_mock_path_list()

    def _get_mock_path_list(self):
        module_path = PythonDependency.__module__
        return {
            'version': f'{module_path}.version',
            'Requirement': f'{module_path}.Requirement'
        }

    def _get_test_dependency(self, name='test_dependency', version_string=''):
        dependency = PythonDependency.__new__(PythonDependency)
        dependency.name = name
        dependency.version_string = version_string
        return dependency

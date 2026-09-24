from mayan.apps.app_manager.apps import MayanAppConfig
from mayan.apps.dashboards.dashboards import dashboard_administrator

from .dashboard_widgets import DashboardWidgetActivityByUser


class AnalyticsApp(MayanAppConfig):
    app_namespace = 'analytics'
    app_url = 'analytics'
    has_rest_api = False
    has_tests = True
    name = 'mayan.apps.analytics'
    verbose_name = 'Analytics'

    def ready(self):
        super().ready()

        dashboard_administrator.add_widget(
            widget=DashboardWidgetActivityByUser, order=100
        )

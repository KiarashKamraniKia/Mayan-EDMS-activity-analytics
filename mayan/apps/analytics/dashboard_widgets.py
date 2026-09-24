from mayan.apps.dashboards.classes import BaseDashboardWidget



class DashboardWidgetActivityByUser(BaseDashboardWidget):
    label = 'Activity by User'
    template_name = 'analytics/dashboard_activity_by_user.html'

    def get_base_context(self):
        from .analytics import activity_by_user
        return {
            'object_list': activity_by_user()
        }

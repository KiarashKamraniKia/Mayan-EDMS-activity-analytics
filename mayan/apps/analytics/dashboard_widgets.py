from mayan.apps.dashboards.classes import BaseDashboardWidget


class DashboardWidgetActivityByUser(BaseDashboardWidget):
    label = 'Activity by User'
    template_name = 'analytics/dashboard_activity_by_user.html'

    def get_base_context(self):
        from .analytics import activity_by_user
        return {
            'object_list': activity_by_user()
        }


class DashboardWidgetActivityByEventType(BaseDashboardWidget):
    label = 'Activity by Event Type'
    template_name = 'analytics/dashboard_activity_by_event_type.html'

    def get_base_context(self):
        from .analytics import activity_by_event_type
        return {
            'object_list': activity_by_event_type()
        }


class DashboardWidgetActivityTrend(BaseDashboardWidget):
    label = 'Activity Trend'
    template_name = 'statistics/renderers/chartjs/base.html'

    def get_base_context(self):
        from mayan.apps.mayan_statistics.classes import StatisticType

        statistic = StatisticType.get('activity-trend')

        return {
            'chart_context': statistic.get_chart_context()
        }

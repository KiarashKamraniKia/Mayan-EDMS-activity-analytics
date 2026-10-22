from mayan.apps.dashboards.classes import BaseDashboardWidget


class DashboardWidgetActivityByUser(BaseDashboardWidget):
    label = 'Activity by User'
    template_name = 'analytics/dashboard_activity_by_user.html'

    def get_base_context(self):
        from django.contrib.auth import get_user_model

        from .analytics import activity_by_user

        rows = list(activity_by_user())
        user_ids = [int(row['actor_object_id']) for row in rows]
        users = get_user_model().objects.in_bulk(user_ids)

        for row in rows:
            user_id = int(row['actor_object_id'])
            user = users.get(user_id)
            row['username'] = (
                user.get_username()
                if user else f'Unknown user ({user_id})'
            )

        return {
            'object_list': rows
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

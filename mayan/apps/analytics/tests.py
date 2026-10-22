from datetime import datetime, timezone as datetime_timezone
from unittest.mock import patch, sentinel

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.test import SimpleTestCase, TestCase
from django.utils import timezone

from actstream.models import Action

from mayan.apps.mayan_statistics.classes import (
    StatisticType,
    StatisticTypeLineChart
)

from .analytics import (
    activity_by_event_type,
    activity_by_user,
    activity_trend as query_activity_trend
)
from .dashboard_widgets import (
    DashboardWidgetActivityByEventType,
    DashboardWidgetActivityByUser,
    DashboardWidgetActivityTrend
)
from .statistics import activity_trend as statistics_activity_trend


UTC = datetime_timezone.utc


class ActivityAnalyticsDatabaseTests(TestCase):
    """Integration tests using actual Action records and SQL aggregation."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.user_a = User.objects.create(username='analytics_user_a')
        cls.user_b = User.objects.create(username='analytics_user_b')

        # A Group is a valid generic actor, but is not a User.
        cls.group_actor = Group.objects.create(
            name='analytics_non_user_actor'
        )

    def create_activity(
        self,
        verb,
        actor=None,
        timestamp=None
    ):
        if actor is None:
            actor = self.user_a

        if timestamp is None:
            timestamp = datetime(2026, 1, 2, 10, tzinfo=UTC)

        return Action.objects.create(
            actor_content_type=ContentType.objects.get_for_model(
                type(actor)
            ),
            actor_object_id=str(actor.pk),
            verb=verb,
            timestamp=timestamp
        )

    def test_activity_by_user_empty_database(self):
        self.assertEqual(list(activity_by_user()), [])

    def test_activity_by_user_counts_and_descending_order(self):
        for _ in range(3):
            self.create_activity('documents.document_create')

        self.create_activity(
            'documents.document_delete',
            actor=self.user_b
        )

        self.assertEqual(
            list(activity_by_user()),
            [
                {
                    'actor_object_id': str(self.user_a.pk),
                    'activity_count': 3
                },
                {
                    'actor_object_id': str(self.user_b.pk),
                    'activity_count': 1
                }
            ]
        )

    def test_activity_by_user_excludes_unrelated_events_and_actors(self):
        self.create_activity('documents.document_create')
        self.create_activity('authentication.login')

        self.create_activity(
            'documents.document_delete',
            actor=self.group_actor
        )

        self.assertEqual(
            list(activity_by_user()),
            [
                {
                    'actor_object_id': str(self.user_a.pk),
                    'activity_count': 1
                }
            ]
        )

    def test_activity_by_event_type_empty_database(self):
        self.assertEqual(list(activity_by_event_type()), [])

    def test_activity_by_event_type_groups_counts_and_orders(self):
        for _ in range(3):
            self.create_activity('documents.document_create')

        self.create_activity(
            'documents.document_delete',
            actor=self.user_b
        )

        self.create_activity('authentication.login')
        self.create_activity('authentication.login')

        self.assertEqual(
            list(activity_by_event_type()),
            [
                {
                    'verb': 'documents.document_create',
                    'activity_count': 3
                },
                {
                    'verb': 'documents.document_delete',
                    'activity_count': 1
                }
            ]
        )

    def test_event_type_includes_non_user_actors(self):
        self.create_activity(
            'documents.document_create',
            actor=self.group_actor
        )

        self.assertEqual(
            list(activity_by_event_type()),
            [
                {
                    'verb': 'documents.document_create',
                    'activity_count': 1
                }
            ]
        )

    def test_activity_trend_empty_database(self):
        self.assertEqual(list(query_activity_trend()), [])

    def test_activity_trend_aggregates_by_day_and_orders_dates(self):
        day_one_morning = datetime(2026, 1, 2, 9, tzinfo=UTC)
        day_one_evening = datetime(2026, 1, 2, 19, tzinfo=UTC)
        day_three = datetime(2026, 1, 4, 12, tzinfo=UTC)

        # Insert out of chronological order to verify SQL ordering.
        self.create_activity(
            'documents.document_delete',
            timestamp=day_three
        )

        self.create_activity(
            'documents.document_create',
            timestamp=day_one_morning
        )
        self.create_activity(
            'documents.document_update',
            actor=self.user_b,
            timestamp=day_one_evening
        )
        self.create_activity(
            'authentication.login',
            timestamp=day_one_morning
        )

        with timezone.override(UTC):
            result = [
                (item['day'].date().isoformat(), item['activity_count'])
                for item in query_activity_trend()
            ]

        # The missing January 3 date must not become a fake record.
        self.assertEqual(
            result,
            [
                ('2026-01-02', 2),
                ('2026-01-04', 1)
            ]
        )

    def test_activity_trend_includes_non_user_actors(self):
        self.create_activity(
            'documents.document_create',
            actor=self.group_actor
        )

        with timezone.override(UTC):
            result = list(query_activity_trend())

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['activity_count'], 1)
        self.assertEqual(
            result[0]['day'].date().isoformat(),
            '2026-01-02'
        )

    def test_statistics_returns_empty_series(self):
        with timezone.override(UTC):
            self.assertEqual(
                statistics_activity_trend(),
                {'series': {'Activities': []}}
            )

    def test_statistics_returns_correct_chart_data(self):
        self.create_activity(
            'documents.document_create',
            timestamp=datetime(2026, 1, 4, 10, tzinfo=UTC)
        )
        self.create_activity(
            'documents.document_create',
            timestamp=datetime(2026, 1, 2, 8, tzinfo=UTC)
        )
        self.create_activity(
            'documents.document_update',
            actor=self.user_b,
            timestamp=datetime(2026, 1, 2, 18, tzinfo=UTC)
        )
        self.create_activity(
            'authentication.login',
            timestamp=datetime(2026, 1, 2, 18, tzinfo=UTC)
        )

        with timezone.override(UTC):
            result = statistics_activity_trend()

        self.assertEqual(
            result,
            {
                'series': {
                    'Activities': [
                        {'2026-01-02': 2},
                        {'2026-01-04': 1}
                    ]
                }
            }
        )


class ActivityDashboardWidgetTests(SimpleTestCase):
    """Check widget context contracts without requiring a database."""

    @patch(
        'mayan.apps.analytics.analytics.activity_by_user',
        return_value=sentinel.user_activity_rows
    )
    def test_user_widget_provides_query_result(self, mock_function):
        context = DashboardWidgetActivityByUser.get_base_context(None)

        self.assertEqual(
            context,
            {'object_list': sentinel.user_activity_rows}
        )
        mock_function.assert_called_once_with()

    @patch(
        'mayan.apps.analytics.analytics.activity_by_event_type',
        return_value=sentinel.event_type_rows
    )
    def test_event_type_widget_provides_query_result(
        self, mock_function
    ):
        context = DashboardWidgetActivityByEventType.get_base_context(
            None
        )

        self.assertEqual(
            context,
            {'object_list': sentinel.event_type_rows}
        )
        mock_function.assert_called_once_with()

    @patch(
        'mayan.apps.mayan_statistics.classes.StatisticType.get'
    )
    def test_trend_widget_uses_registered_statistic(
        self, mock_statistic_get
    ):
        mock_statistic = mock_statistic_get.return_value
        mock_statistic.get_chart_context.return_value = (
            sentinel.chart_context
        )

        context = DashboardWidgetActivityTrend.get_base_context(None)

        mock_statistic_get.assert_called_once_with('activity-trend')
        mock_statistic.get_chart_context.assert_called_once_with()

        self.assertEqual(
            context,
            {'chart_context': sentinel.chart_context}
        )

    def test_widget_labels_and_templates(self):
        self.assertEqual(
            DashboardWidgetActivityByUser.label,
            'Activity by User'
        )
        self.assertEqual(
            DashboardWidgetActivityByUser.template_name,
            'analytics/dashboard_activity_by_user.html'
        )

        self.assertEqual(
            DashboardWidgetActivityByEventType.label,
            'Activity by Event Type'
        )
        self.assertEqual(
            DashboardWidgetActivityByEventType.template_name,
            'analytics/dashboard_activity_by_event_type.html'
        )

        self.assertEqual(
            DashboardWidgetActivityTrend.label,
            'Activity Trend'
        )
        self.assertEqual(
            DashboardWidgetActivityTrend.template_name,
            'statistics/renderers/chartjs/base.html'
        )

    def test_activity_trend_statistic_is_registered(self):
        statistic = StatisticType.get('activity-trend')

        self.assertIsInstance(
            statistic,
            StatisticTypeLineChart
        )

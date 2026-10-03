from django.db.models import Count
from django.db.models.functions import TruncDay

from actstream.models import Action
from mayan.apps.mayan_statistics.classes import (
    StatisticNamespace, StatisticTypeLineChart
)


def activity_trend():
    queryset = (
        Action.objects
        .filter(
            verb__startswith='documents.'
        )
        .annotate(
            day=TruncDay('timestamp')
        )
        .values(
            'day'
        )
        .annotate(
            activity_count=Count('id')
        )
        .order_by('day')
    )

    return {
        'series': {
            'Activities': [
                {
                    item['day'].strftime('%Y-%m-%d'): item['activity_count']
                }
                for item in queryset
            ]
        }
    }


namespace = StatisticNamespace(
    slug='analytics', label='Analytics'
)

namespace.add_statistic(
    klass=StatisticTypeLineChart,
    slug='activity-trend',
    label='Activity Trend',
    func=activity_trend,
    minute='0'
)

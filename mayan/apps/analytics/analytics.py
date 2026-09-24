from django.contrib.contenttypes.models import ContentType
from django.db.models import Count

from actstream.models import Action
from django.contrib.auth.models import User


def activity_by_user():
    user_content_type = ContentType.objects.get_for_model(User)

    return (
        Action.objects
        .filter(
            actor_content_type=user_content_type,
            verb__startswith='documents.'
        )
        .values(
            'actor_object_id'
        )
        .annotate(
            activity_count=Count('id')
        )
        .order_by('-activity_count')
    )


def activity_by_event_type():
    return (
        Action.objects
        .filter(
            verb__startswith='documents.'
        )
        .values(
            'verb'
        )
        .annotate(
            activity_count=Count('id')
        )
        .order_by('-activity_count')
    )
from datetime import timedelta

from dateutil.parser import parse

from django.template import Library

register = Library()


@register.filter(name='date_parse')
def filter_date_parse(date_string):
    """
    Takes a string and converts it into a datetime object.
    """
    return parse(timestr=date_string)


@register.simple_tag(name='timedelta')
def tag_timedelta(date, **kwargs):
    """
    Takes a datetime object and applies a timedelta.
    """
    return date + timedelta(**kwargs)

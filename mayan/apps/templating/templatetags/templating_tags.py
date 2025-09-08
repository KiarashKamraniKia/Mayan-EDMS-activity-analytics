from django.template import Library, Node, TemplateSyntaxError
from django.utils.html import strip_spaces_between_tags
from django.utils.translation import gettext_lazy as _

from ..decorators import templating_dangerous_tag

register = Library()

# Filters


@register.filter(name='dict_get')
def filter_dict_get(dictionary, key):
    """
    Return the value for the given key or '' if not found.
    """
    return dictionary.get(key, '')


@register.filter(name='split')
def filter_split(obj, separator):
    """
    Return a list of the words in the string, using sep as the delimiter
    string.
    """
    return obj.split(separator)


# Tags


class SpacelessPlusNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        content = self.nodelist.render(context).strip()
        result = []
        for line in content.split('\n'):
            if line.strip() != '':
                result.append(line)

        return strip_spaces_between_tags(
            value='\n'.join(result)
        )


@register.simple_tag(name='method')
@templating_dangerous_tag(
    reason=_(
        message='Tag can bypass access controls and create permanent changes.'
    )
)
def tag_method(obj, method, *args, **kwargs):
    """
    Call an object method. {% method object method **kwargs %}
    """
    try:
        return getattr(obj, method)(*args, **kwargs)
    except Exception as exception:
        raise TemplateSyntaxError(
            'Error calling object method; {}'.format(exception)
        )


@register.simple_tag(name='set')
def tag_set(value):
    """
    Set a context variable to a specific value.
    """
    return value


@register.tag(name='spaceless_plus')
def tag_spaceless_plus(parser, token):
    """
    Removes empty lines between the tag nodes.
    """
    nodelist = parser.parse(
        ('endspaceless_plus',)
    )
    parser.delete_first_token()
    return SpacelessPlusNode(nodelist=nodelist)

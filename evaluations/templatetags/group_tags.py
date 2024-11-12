#
from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Returns True if the user is in the given group, else False.
    Usage in template: {% if user|has_group:"Manager" %}
    """
    return user.groups.filter(name=group_name).exists()
#cloner174
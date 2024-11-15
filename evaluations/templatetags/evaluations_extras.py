from django import template

register = template.Library()

@register.filter
def get_field(fields, field_name):
    return fields.get(field_name)

@register.filter
def to_list(start, end):
    return range(start, end + 1)

#cloner174
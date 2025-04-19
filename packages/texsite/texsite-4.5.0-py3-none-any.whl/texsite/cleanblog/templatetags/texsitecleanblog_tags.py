from django import template


register = template.Library()


@register.filter
def inlinecode(value: str) -> str:
    while value.count('`') >= 2:
        value = value.replace('`', '<code>', 1).replace('`', '</code>', 1)

    return value

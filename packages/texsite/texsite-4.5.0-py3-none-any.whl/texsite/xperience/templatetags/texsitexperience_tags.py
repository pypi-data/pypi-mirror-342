from django import template
from wagtail.core.models import Page


register = template.Library()


@register.simple_tag
def get_live_descendant_pages(
    parent: Page, limit: int = 0, newest_first: bool = False
) -> list[Page]:
    order_by = '-first_published_at' if newest_first else 'first_published_at'

    return parent.get_descendants().live().order_by(order_by)[:limit]

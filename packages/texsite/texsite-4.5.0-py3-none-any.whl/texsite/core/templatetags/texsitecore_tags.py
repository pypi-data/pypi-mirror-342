from django import template

from texsite.core.models import BasePage


register = template.Library()


@register.simple_tag
def get_footer_pages(site):
    return BasePage.objects.in_site(site).live().filter(show_in_footer=True)


@register.simple_tag
def get_menu_pages(site):
    return BasePage.objects.in_site(site).live().filter(show_in_menus=True)

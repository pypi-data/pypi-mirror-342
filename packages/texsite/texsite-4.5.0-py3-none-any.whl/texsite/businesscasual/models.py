from django.utils.translation import ugettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from texsite.core.models import BasePage
from .blocks import ContactBlock, ContentBlock, DocumentsBlock, PeopleBlock


class BusinessCasualPage(BasePage):
    body = StreamField(
        [
            ('content', ContentBlock()),
            ('documents', DocumentsBlock()),
            ('people', PeopleBlock()),
            ('contact', ContactBlock()),
        ],
        use_json_field=True,
    )

    content_panels = BasePage.content_panels + [FieldPanel('body')]
    password_required_template = 'texsitebusinesscasual/login_password.html'

    class Meta:
        verbose_name = _('Business Casual Page') + ' (' + __package__ + ')'

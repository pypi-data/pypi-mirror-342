from django.db.models import BooleanField
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.search.index import FilterField


class BasePage(Page):
    is_creatable = False

    show_in_footer = BooleanField(
        verbose_name=_('show in footer'),
        default=False,
        help_text=_(
            'Whether a link to this page will appear in automatically '
            'generated footers'
        ),
    )

    search_fields = Page.search_fields + [
        FilterField('show_in_footer'),
    ]
    promote_panels = [
        MultiFieldPanel(
            [
                FieldPanel('slug'),
                FieldPanel('seo_title'),
                FieldPanel('search_description'),
            ],
            _('For search engines'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('first_published_at'),
            ],
            _('Timeline'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('show_in_menus'),
                FieldPanel('show_in_footer'),
            ],
            _('For site menus'),
        ),
    ]

    @property
    def next_sibling(self):
        return self.get_next_siblings().live().first()

    @property
    def previous_sibling(self):
        return self.get_prev_siblings().live().first()

    class Meta:
        verbose_name = _('Base Page') + ' (' + __package__ + ')'

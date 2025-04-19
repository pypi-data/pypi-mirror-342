from django.utils.translation import ugettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import (
    BooleanBlock,
    IntegerBlock,
    ListBlock,
    PageChooserBlock,
    RawHTMLBlock,
    RichTextBlock,
    StructBlock,
)
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock

from texsite.core.blocks import PromotedPageBlock
from texsite.core.models import BasePage


class XperiencePage(BasePage):
    body = StreamField(
        [
            ('paragraph', RichTextBlock(icon='pilcrow')),
            (
                'teaser_image',
                ImageChooserBlock(
                    template='texsitexperience/blocks/teaser_image.html',
                    icon='image',
                ),
            ),
            (
                'carousel',
                ListBlock(
                    ImageChooserBlock(),
                    min_num=2,
                    template='texsitexperience/blocks/carousel.html',
                    icon='image',
                ),
            ),
            (
                'promoted_pages',
                ListBlock(
                    PromotedPageBlock(),
                    template='texsitexperience/blocks/promoted_pages.html',
                    icon='pick',
                ),
            ),
            (
                'article_listing',
                StructBlock(
                    [
                        ('parent', PageChooserBlock()),
                        ('limit', IntegerBlock(required=False, min_value=1)),
                        (
                            'newest_first',
                            BooleanBlock(default=True, required=False),
                        ),
                    ],
                    template='texsitexperience/blocks/article_listing.html',
                    icon='list-ul',
                ),
            ),
            ('raw_html', RawHTMLBlock()),
        ],
        use_json_field=True,
    )

    content_panels = BasePage.content_panels + [FieldPanel('body')]
    password_required_template = 'texsitexperience/login_password.html'

    class Meta:
        verbose_name = _('Xperience Page') + ' (' + __package__ + ')'

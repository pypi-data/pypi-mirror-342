from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import StreamField

from texsite.core.blocks import (
    CodeBlock,
    HeadingBlock,
    ImageBlock,
    IntroBlock,
    QuoteBlock,
)
from texsite.core.models import BasePage


class CleanBlogArticlePage(BasePage):
    body = StreamField(
        [
            (
                'intro',
                IntroBlock(template='texsitecleanblog/blocks/intro.html'),
            ),
            (
                'heading',
                HeadingBlock(template='texsitecleanblog/blocks/heading.html'),
            ),
            ('paragraph', RichTextBlock()),
            (
                'image',
                ImageBlock(template='texsitecleanblog/blocks/image.html'),
            ),
            (
                'quote',
                QuoteBlock(template='texsitecleanblog/blocks/quote.html'),
            ),
            (
                'code',
                CodeBlock(template='texsitecleanblog/blocks/code.html'),
            ),
        ],
        use_json_field=True,
    )

    content_panels = BasePage.content_panels + [FieldPanel('body')]

    class Meta:
        verbose_name = _('Clean Blog Article Page') + ' (' + __package__ + ')'


class CleanBlogArticleIndexPage(BasePage):
    body = StreamField(
        [
            (
                'intro',
                IntroBlock(template='texsitecleanblog/blocks/intro.html'),
            ),
        ],
        use_json_field=True,
    )

    @property
    def articles(self):
        return (
            CleanBlogArticlePage.objects.live()
            .descendant_of(self)
            .order_by('-first_published_at')
        )

    def get_context(self, request):
        articles = self.articles
        page = request.GET.get('page')
        paginator = Paginator(articles, per_page=8)

        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context = super(CleanBlogArticleIndexPage, self).get_context(request)
        context['articles'] = articles

        return context

    content_panels = BasePage.content_panels + [FieldPanel('body')]

    class Meta:
        verbose_name = (
            _('Clean Blog Article Index Page') + ' (' + __package__ + ')'
        )

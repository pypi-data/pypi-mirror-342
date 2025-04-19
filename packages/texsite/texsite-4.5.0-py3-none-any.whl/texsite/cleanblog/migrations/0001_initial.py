import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texsitecore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CleanBlogArticlePage',
            fields=[
                (
                    'basepage_ptr',
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        to='texsitecore.BasePage',
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    'body',
                    wagtail.fields.StreamField(
                        [
                            (
                                b'intro',
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            b'keyvisual',
                                            wagtail.images.blocks.ImageChooserBlock(
                                                required=False
                                            ),
                                        ),
                                        (
                                            b'slogan',
                                            wagtail.blocks.CharBlock(
                                                required=True
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            (
                                b'heading',
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            b'title',
                                            wagtail.blocks.CharBlock(
                                                required=True
                                            ),
                                        ),
                                        (
                                            b'subtitle',
                                            wagtail.blocks.CharBlock(
                                                required=False
                                            ),
                                        ),
                                    ],
                                    template=b'texsitecleanblog/blocks/heading.html',
                                ),
                            ),
                            (
                                b'paragraph',
                                wagtail.blocks.RichTextBlock(),
                            ),
                            (
                                b'image',
                                wagtail.images.blocks.ImageChooserBlock(
                                    template=b'texsitecleanblog/blocks/image.html'
                                ),
                            ),
                        ]
                    ),
                ),
            ],
            options={
                'verbose_name': 'Clean Blog Article Page (texsite.cleanblog)',
            },
            bases=('texsitecore.basepage',),
        ),
    ]

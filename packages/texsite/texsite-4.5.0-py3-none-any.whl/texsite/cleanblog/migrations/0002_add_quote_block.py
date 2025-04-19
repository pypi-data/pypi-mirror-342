import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texsitecleanblog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cleanblogarticlepage',
            name='body',
            field=wagtail.fields.StreamField(
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
                                    wagtail.blocks.CharBlock(required=True),
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
                                    wagtail.blocks.CharBlock(required=True),
                                ),
                                (
                                    b'subtitle',
                                    wagtail.blocks.CharBlock(required=False),
                                ),
                            ],
                            template=b'texsitecleanblog/blocks/heading.html',
                        ),
                    ),
                    (b'paragraph', wagtail.blocks.RichTextBlock()),
                    (
                        b'image',
                        wagtail.images.blocks.ImageChooserBlock(
                            template=b'texsitecleanblog/blocks/image.html'
                        ),
                    ),
                    (
                        b'quote',
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    b'quote',
                                    wagtail.blocks.TextBlock(required=True),
                                ),
                                (
                                    b'originator',
                                    wagtail.blocks.CharBlock(required=False),
                                ),
                            ],
                            template=b'texsitecleanblog/blocks/quote.html',
                        ),
                    ),
                ]
            ),
        ),
    ]

import json

import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models


def convert_to_imageblock(apps, schema_editor):
    CleanBlogArticlePage = apps.get_model(
        'texsitecleanblog', 'CleanBlogArticlePage'
    )

    for page in CleanBlogArticlePage.objects.all():
        new_stream_data = []

        for block in page.body.stream_data:
            if block['type'] == 'image':
                extendedimage = {
                    'type': 'extendedimage',
                    'value': {'image': block['value']},
                }
                new_stream_data.append(extendedimage)
            else:
                new_stream_data.append(block)

        page.body = json.dumps(new_stream_data)
        page.save()


def rename_imageblock(apps, schema_editor):
    CleanBlogArticlePage = apps.get_model(
        'texsitecleanblog', 'CleanBlogArticlePage'
    )

    for page in CleanBlogArticlePage.objects.all():
        new_stream_data = []

        for block in page.body.stream_data:
            if block['type'] == 'extendedimage':
                block['type'] = 'image'

            new_stream_data.append(block)

        page.body = json.dumps(new_stream_data)
        page.save()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('texsitecleanblog', '0002_add_quote_block'),
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
                        b'extendedimage',
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    b'image',
                                    wagtail.images.blocks.ImageChooserBlock(
                                        required=True
                                    ),
                                ),
                                (
                                    b'caption',
                                    wagtail.blocks.CharBlock(required=False),
                                ),
                            ],
                            template=b'texsitecleanblog/blocks/image.html',
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
        migrations.RunPython(
            convert_to_imageblock,
            noop,
        ),
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
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    b'image',
                                    wagtail.images.blocks.ImageChooserBlock(
                                        required=True
                                    ),
                                ),
                                (
                                    b'caption',
                                    wagtail.blocks.CharBlock(required=False),
                                ),
                            ],
                            template=b'texsitecleanblog/blocks/image.html',
                        ),
                    ),
                    (
                        b'extendedimage',
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    b'image',
                                    wagtail.images.blocks.ImageChooserBlock(
                                        required=True
                                    ),
                                ),
                                (
                                    b'caption',
                                    wagtail.blocks.CharBlock(required=False),
                                ),
                            ],
                            template=b'texsitecleanblog/blocks/image.html',
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
        migrations.RunPython(
            rename_imageblock,
            noop,
        ),
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
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    b'image',
                                    wagtail.images.blocks.ImageChooserBlock(
                                        required=True
                                    ),
                                ),
                                (
                                    b'caption',
                                    wagtail.blocks.CharBlock(required=False),
                                ),
                            ],
                            template=b'texsitecleanblog/blocks/image.html',
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

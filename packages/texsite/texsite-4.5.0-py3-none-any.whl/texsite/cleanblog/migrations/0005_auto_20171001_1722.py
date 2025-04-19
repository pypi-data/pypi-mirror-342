import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texsitecleanblog', '0004_cleanblogarticleindexpage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cleanblogarticleindexpage',
            options={
                'verbose_name': 'Clean Blog Artikel Übersicht (texsite.cleanblog)'
            },
        ),
        migrations.AlterModelOptions(
            name='cleanblogarticlepage',
            options={
                'verbose_name': 'Clean Blog Artikel Seite (texsite.cleanblog)'
            },
        ),
        migrations.AlterField(
            model_name='cleanblogarticleindexpage',
            name='body',
            field=wagtail.fields.StreamField(
                (
                    (
                        'intro',
                        wagtail.blocks.StructBlock(
                            (
                                (
                                    'keyvisual',
                                    wagtail.images.blocks.ImageChooserBlock(
                                        required=False
                                    ),
                                ),
                                (
                                    'slogan',
                                    wagtail.blocks.CharBlock(required=True),
                                ),
                            ),
                            template='texsitecleanblog/blocks/intro.html',
                        ),
                    ),
                )
            ),
        ),
        migrations.AlterField(
            model_name='cleanblogarticlepage',
            name='body',
            field=wagtail.fields.StreamField(
                (
                    (
                        'intro',
                        wagtail.blocks.StructBlock(
                            (
                                (
                                    'keyvisual',
                                    wagtail.images.blocks.ImageChooserBlock(
                                        required=False
                                    ),
                                ),
                                (
                                    'slogan',
                                    wagtail.blocks.CharBlock(required=True),
                                ),
                            ),
                            template='texsitecleanblog/blocks/intro.html',
                        ),
                    ),
                    (
                        'heading',
                        wagtail.blocks.StructBlock(
                            (
                                (
                                    'title',
                                    wagtail.blocks.CharBlock(required=True),
                                ),
                                (
                                    'subtitle',
                                    wagtail.blocks.CharBlock(required=False),
                                ),
                            ),
                            template='texsitecleanblog/blocks/heading.html',
                        ),
                    ),
                    ('paragraph', wagtail.blocks.RichTextBlock()),
                    (
                        'image',
                        wagtail.blocks.StructBlock(
                            (
                                (
                                    'image',
                                    wagtail.images.blocks.ImageChooserBlock(
                                        required=True
                                    ),
                                ),
                                (
                                    'caption',
                                    wagtail.blocks.CharBlock(required=False),
                                ),
                            ),
                            template='texsitecleanblog/blocks/image.html',
                        ),
                    ),
                    (
                        'quote',
                        wagtail.blocks.StructBlock(
                            (
                                (
                                    'quote',
                                    wagtail.blocks.TextBlock(required=True),
                                ),
                                (
                                    'originator',
                                    wagtail.blocks.CharBlock(required=False),
                                ),
                            ),
                            template='texsitecleanblog/blocks/quote.html',
                        ),
                    ),
                )
            ),
        ),
    ]

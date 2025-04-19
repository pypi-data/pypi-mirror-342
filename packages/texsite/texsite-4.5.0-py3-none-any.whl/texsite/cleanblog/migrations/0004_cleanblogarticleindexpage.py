import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texsitecore', '0001_initial'),
        ('texsitecleanblog', '0003_change_image_to_image_block'),
    ]

    operations = [
        migrations.CreateModel(
            name='CleanBlogArticleIndexPage',
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
                            )
                        ]
                    ),
                ),
            ],
            options={
                'verbose_name': 'Clean Blog Article Index Page (texsite.cleanblog)',
            },
            bases=('texsitecore.basepage',),
        ),
    ]

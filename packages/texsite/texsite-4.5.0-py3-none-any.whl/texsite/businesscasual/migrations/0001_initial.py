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
            name='BusinessCasualPage',
            fields=[
                (
                    'basepage_ptr',
                    models.OneToOneField(
                        to='texsitecore.BasePage',
                        primary_key=True,
                        parent_link=True,
                        serialize=False,
                        auto_created=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    'body',
                    wagtail.fields.StreamField(
                        (
                            (
                                'content',
                                wagtail.blocks.StructBlock(
                                    (
                                        (
                                            'heading',
                                            wagtail.blocks.CharBlock(
                                                required=True
                                            ),
                                        ),
                                        (
                                            'image',
                                            wagtail.images.blocks.ImageChooserBlock(
                                                required=False
                                            ),
                                        ),
                                        (
                                            'paragraph',
                                            wagtail.blocks.RichTextBlock(
                                                required=True
                                            ),
                                        ),
                                    )
                                ),
                            ),
                        )
                    ),
                ),
            ],
            options={
                'verbose_name': 'Business Casual Page (texsite.businesscasual)',
            },
            bases=('texsitecore.basepage',),
        ),
    ]

import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texsitebusinesscasual', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesscasualpage',
            name='body',
            field=wagtail.fields.StreamField(
                (
                    (
                        'content',
                        wagtail.blocks.StructBlock(
                            (
                                (
                                    'heading',
                                    wagtail.blocks.CharBlock(required=True),
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
                    (
                        'documents',
                        wagtail.blocks.StructBlock(
                            (
                                (
                                    'heading',
                                    wagtail.blocks.CharBlock(required=True),
                                ),
                                (
                                    'paragraph',
                                    wagtail.blocks.RichTextBlock(
                                        required=False
                                    ),
                                ),
                                (
                                    'files',
                                    wagtail.blocks.ListBlock(
                                        wagtail.documents.blocks.DocumentChooserBlock(),
                                        template='texsitebusinesscasual/blocks/documentlist.html',
                                    ),
                                ),
                            )
                        ),
                    ),
                )
            ),
        ),
    ]

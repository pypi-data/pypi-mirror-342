from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texsitecore', '0002_alter_basepage_options'),
    ]

    operations = [
        migrations.RunSQL('DROP TABLE IF EXISTS wagtailmenus_mainmenuitem;'),
        migrations.RunSQL('DROP TABLE IF EXISTS wagtailmenus_mainmenu;'),
        migrations.RunSQL('DROP TABLE IF EXISTS wagtailmenus_flatmenuitem;'),
        migrations.RunSQL('DROP TABLE IF EXISTS wagtailmenus_flatmenu;'),
    ]

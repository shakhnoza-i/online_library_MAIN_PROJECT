# Generated by Django 3.2.5 on 2021-08-02 07:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0007_auto_20210801_1137'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WatchList',
            new_name='Book',
        ),
        migrations.RenameModel(
            old_name='StreamPlatform',
            new_name='OnlineLibrary',
        ),
    ]

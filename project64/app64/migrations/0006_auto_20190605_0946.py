# Generated by Django 2.1.5 on 2019-06-05 01:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app64', '0005_auto_20190605_0940'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='Info',
            new_name='B_Info',
        ),
    ]
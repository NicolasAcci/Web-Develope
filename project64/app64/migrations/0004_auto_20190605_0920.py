# Generated by Django 2.1.5 on 2019-06-05 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app64', '0003_auto_20190605_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='info',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='book',
            name='art_path',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='book_name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='use_name',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]

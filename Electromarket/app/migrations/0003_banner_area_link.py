# Generated by Django 4.1.7 on 2023-02-18 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_banner_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner_area',
            name='Link',
            field=models.CharField(max_length=200, null=True),
        ),
    ]

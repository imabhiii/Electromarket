# Generated by Django 4.1.7 on 2023-02-23 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_alter_productreview_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productreview',
            name='created_at',
        ),
        migrations.AddField(
            model_name='productreview',
            name='email',
            field=models.EmailField(default=0, max_length=100),
        ),
    ]

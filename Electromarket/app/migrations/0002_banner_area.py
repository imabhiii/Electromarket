# Generated by Django 4.1.7 on 2023-02-18 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='banner_area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media/banner_img')),
                ('Discount_Deal', models.CharField(max_length=100)),
                ('Quote', models.CharField(max_length=100)),
                ('Discount', models.IntegerField()),
            ],
        ),
    ]

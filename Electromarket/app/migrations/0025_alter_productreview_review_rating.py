# Generated by Django 4.1.7 on 2023-03-09 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_alter_order_amount_alter_orderitem_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='review_rating',
            field=models.IntegerField(default=5),
        ),
    ]

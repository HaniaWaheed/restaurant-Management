# Generated by Django 5.1.6 on 2025-02-23 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_order_items_order_table_order_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

# Generated by Django 4.0.5 on 2022-06-15 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app0', '0008_alter_order_price'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='order',
            unique_together=set(),
        ),
    ]

# Generated by Django 4.0.5 on 2022-06-15 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app0', '0005_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.SmallIntegerField(choices=[(1, '未完成'), (2, '完成')], default=1, verbose_name='订单状态'),
            preserve_default=False,
        ),
    ]
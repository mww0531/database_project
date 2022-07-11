# Generated by Django 4.0.5 on 2022-06-15 05:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app0', '0006_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='成交价格'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='iid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app0.items', verbose_name='商品ID'),
        ),
        migrations.AlterField(
            model_name='order',
            name='trade_count',
            field=models.SmallIntegerField(default=1, verbose_name='成交数量'),
        ),
    ]
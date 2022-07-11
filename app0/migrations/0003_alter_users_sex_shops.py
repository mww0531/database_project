# Generated by Django 4.0.5 on 2022-06-14 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app0', '0002_alter_users_level_alter_users_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='sex',
            field=models.SmallIntegerField(choices=[(1, '男'), (2, '女')], verbose_name='性别'),
        ),
        migrations.CreateModel(
            name='Shops',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False, verbose_name='店铺ID')),
                ('name', models.CharField(max_length=32, verbose_name='店铺名称')),
                ('status', models.SmallIntegerField(default=0)),
                ('boss', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app0.users', verbose_name='店铺老板')),
            ],
        ),
    ]
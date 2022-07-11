from django.db import models


# Create your models here.

class Users(models.Model):
    id = models.CharField(verbose_name='账户', max_length=32, primary_key=True)
    name = models.CharField(verbose_name='姓名', max_length=32)
    birthdate = models.DateField(verbose_name='生日', blank=True, null=True)
    gender = [
        (1, '男'),
        (2, '女'),
    ]
    sex = models.SmallIntegerField(verbose_name='性别', choices=gender, blank=True, null=True)
    phone_number = models.CharField(verbose_name='电话号码', max_length=20, blank=True, null=True)
    level_choice = [
        (1, '用户'),
        (2, '商家'),
        (3, '管理员'),
    ]
    level = models.SmallIntegerField(verbose_name='级别', default=0, choices=level_choice)
    password = models.CharField(verbose_name='密码', max_length=20)

    def __str__(self):
        return self.id


class Shops(models.Model):
    id = models.CharField(verbose_name='店铺ID', max_length=32, primary_key=True)
    name = models.CharField(verbose_name='店铺名称', max_length=32)
    boss = models.ForeignKey(verbose_name='店铺老板', to='Users', to_field='id', on_delete=models.CASCADE, blank=True,
                             null=True)
    status = models.SmallIntegerField(default=0)  # 0没开店 1开店

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    name = models.CharField(verbose_name="仓库名称", max_length=32)
    address = models.CharField(verbose_name="仓库地址", max_length=32)

    def __str__(self):
        return str(self.name)


class Items(models.Model):
    name = models.CharField(verbose_name='商品名称', max_length=32)
    shop = models.ForeignKey(verbose_name='店铺ID', to='Shops', to_field='id', on_delete=models.CASCADE, blank=True,
                             null=True)
    category_choice = [
        (1, '食品'),
        (2, '服装'),
        (3, '日用品'),
        (4, '家具'),
        (5, '电子设备'),
        (6, '纺织品'),
        (7, '图书'),
        (8, '其他'),
    ]
    category = models.SmallIntegerField(verbose_name='商品类别', choices=category_choice, )
    price = models.DecimalField(verbose_name='商品价格', max_digits=10, decimal_places=2)
    count = models.BigIntegerField(verbose_name="商品数量")
    warehouse = models.ForeignKey(verbose_name="所在仓库", to='Warehouse', to_field='id', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    uid = models.ForeignKey(verbose_name="用户ID", to='Users', to_field='id', on_delete=models.CASCADE)
    iid = models.ForeignKey(verbose_name="商品ID", to='Items', to_field='id', on_delete=models.CASCADE)
    trade_time = models.DateTimeField(verbose_name="成交日期")
    trade_count = models.SmallIntegerField(verbose_name='成交数量', default=1)
    gender = [
        (1, '未完成'),
        (2, '完成'),
    ]
    status = models.SmallIntegerField(verbose_name='订单状态', choices=gender)
    price = models.DecimalField(verbose_name='成交价格', max_digits=10, decimal_places=2, null=True, blank=True)

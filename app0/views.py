from django.shortcuts import render, HttpResponse, redirect
from app0 import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app0.pagination import Pagination
from app0.bootstrap import BootStrapModelForm
from django.db.models import Count
import time


# Users表的类

class UsersModel(BootStrapModelForm):
    phone_number = forms.CharField(label="电话号码", validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')])

    # disabled=true 即属性不可编辑
    class Meta:
        model = models.Users
        fields = ['id', 'name', 'birthdate', 'sex', 'phone_number', 'level', 'password']


class UsersModel_edit(BootStrapModelForm):
    phone_number = forms.CharField(label="电话号码", validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')])

    class Meta:
        model = models.Users
        fields = ['name', 'birthdate', 'sex', 'phone_number', 'password']

    # def clean_id(self):
    #     txt_id = self.cleaned_data['id']
    #     if txt_id is True:
    #         obj=models.Users.objects.filter(id=)
    #     return txt_id


class UsersModel_edit_admin(BootStrapModelForm):
    phone_number = forms.CharField(label="电话号码", validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')])

    class Meta:
        model = models.Users
        fields = ['name', 'birthdate', 'sex', 'phone_number', 'level', 'password']


class ShopsModel(BootStrapModelForm):
    class Meta:
        model = models.Shops
        fields = ['id', 'name', 'boss']


class ShopsModel_add(BootStrapModelForm):
    class Meta:
        model = models.Shops
        fields = ['id', 'name']


class ShopsModel_edit_user(BootStrapModelForm):
    class Meta:
        model = models.Shops
        fields = ['name', 'boss']


class ShopsModel_edit_admin(BootStrapModelForm):
    class Meta:
        model = models.Shops
        fields = ['name']


class ItemsModel(BootStrapModelForm):
    id = forms.CharField(label="商品ID", empty_value=True)

    class Meta:
        model = models.Items
        fields = ['id', 'name', 'category', 'price', 'count', 'shop', 'warehouse']

    def clean_price(self):
        txt_price = self.cleaned_data['price']
        if txt_price < 0:
            raise ValidationError("价格不得小于0")
        return txt_price

    def clean_count(self):
        txt_count = self.cleaned_data['count']
        if txt_count < 0:
            raise ValidationError("数量不得小于0")
        return txt_count

    def clean_shop(self):
        txt_shop = self.cleaned_data['shop']
        if txt_shop is None:
            return None
        return txt_shop


class WarehouseModel(BootStrapModelForm):
    id = forms.CharField(label="仓库ID", empty_value=True)

    class Meta:
        model = models.Warehouse
        fields = ['id', 'name', 'address']


class OrderModel(BootStrapModelForm):
    class Meta:
        model = models.Order
        fields = ['uid', 'iid', 'trade_time', 'trade_count', 'status', 'price']

    def clean_count(self):
        txt_count = self.cleaned_data['trade_count']
        if txt_count < 0:
            raise ValidationError("数量不得小于0")
        return txt_count

    def clean_price(self):
        txt_count = self.cleaned_data['trade_count']
        txt_iid = self.cleaned_data['iid'].id
        item_price = models.Items.objects.filter(id=txt_iid).first().price
        txt_price = txt_count * item_price
        return txt_price


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    id = request.POST.get('id')
    pwd = request.POST.get('pwd')
    user = models.Users.objects.filter(id=id, password=pwd).first()
    if user is not None:
        request.session['info'] = {'id': user.id, 'name': user.name, 'level': user.level}
        if user.level == 3:
            return redirect('/admin_home')
        return redirect('/user_home')

    return render(request, 'index.html', {"error": "用户名或密码错误"})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    id = request.POST.get('id')
    name = request.POST.get('name')
    pwd = request.POST.get('f_pwd')
    dpwd = request.POST.get('s_pwd')
    user = models.Users.objects.filter(id=id).exists()
    error = '信息输入不完整'
    if id and name and pwd and dpwd:
        error = '该账号已存在'
        if user is False:
            error = '密码输入不一致'
            if pwd == dpwd:
                new_user = models.Users.objects.create(id=id, name=name, level=1, password=pwd)
                if new_user:
                    return redirect("/")
                error = '创建失败'

    return render(request, 'register.html', {"error": error})


def logout(request):
    request.session.clear()
    return redirect('/')


def user_info(request, nid):
    obj = models.Users.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = UsersModel_edit(instance=obj)
        return render(request, 'user_info.html', {"form": form})
    form = UsersModel_edit(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        request.session.clear()
        request.session['info'] = {'id': obj.id, 'name': obj.name, 'level': obj.level}
        return redirect('/user_home')
    return render(request, 'user_info.html', {"form": form})


def admin_info(request, nid):
    obj = models.Users.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = UsersModel_edit(instance=obj)
        return render(request, 'admin_info.html', {"form": form})
    form = UsersModel_edit(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        request.session.clear()
        request.session['info'] = {'id': obj.id, 'name': obj.name, 'level': obj.level}
        return redirect('/admin_home')
    return render(request, 'admin_info.html', {"form": form})


def user_home(request):
    data_dict = {}
    search_data = request.GET.get('q', "")
    category = request.GET.get('category', '0')
    sort = request.GET.get('sort', '0')
    if search_data:
        data_dict['name__contains'] = search_data
    items = models.Items.objects.all().filter(**data_dict)
    if category and int(category) > 0:
        items = items.filter(category=int(category))
    if sort and int(sort) == 1:
        items = items.order_by('price')
    if sort and int(sort) == 2:
        items = items.order_by('-price')
    count = items.aggregate(item_count=Count('id'))
    page_object = Pagination(request, items)
    context = {
        "search_data": search_data,
        "users": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),  # 页码
        "cate": int(category),
        "sort": int(sort),
        "count": count['item_count']
    }
    return render(request, 'user_home.html', context)


def admin_home(request):
    # for i in range(100):
    #     models.Users.objects.create(id=str(i),name=12334,sex=1,phone_number='16123456789',level=1,password='1')
    data_dict = {}
    search_data = request.GET.get('q', "")

    if search_data:
        data_dict['id__contains'] = search_data
    users = models.Users.objects.all().filter(**data_dict).order_by("-level")
    page_object = Pagination(request, users)
    context = {
        "search_data": search_data,
        "users": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request, 'admin_home.html', context)


def user_add(request):
    if request.method == "GET":
        form = UsersModel()
        return render(request, "user_add.html", {"form": form})
    form = UsersModel(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin_home')
    return render(request, 'user_add.html', {"form": form})


def user_edit(request, nid):
    obj = models.Users.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = UsersModel_edit_admin(instance=obj)
        return render(request, 'user_edit.html', {"form": form})
    form = UsersModel_edit_admin(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        request.session.clear()
        request.session['info'] = {'id': obj.id, 'name': obj.name, 'level': obj.level}
        return redirect('/admin_home')
    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, nid):
    models.Users.objects.filter(id=nid).delete()
    return redirect('/admin_home')


def shop_list(request):
    # for i in range(100):
    #     models.Users.objects.create(id=str(i),name=12334,sex=1,phone_number='16123456789',level=1,password='1')
    data_dict = {}
    search_data = request.GET.get('q', "")

    if search_data:
        data_dict['id__contains'] = search_data
    shops = models.Shops.objects.all().exclude(status=0).filter(**data_dict)
    page_object = Pagination(request, shops)
    context = {
        "search_data": search_data,
        "users": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request, 'shop_list.html', context)


def shop_add(request):
    if request.method == "GET":
        form = ShopsModel()
        return render(request, "shop_add.html", {"form": form})
    form = ShopsModel(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/shop/list')
    return render(request, 'shop_add.html', {"form": form})


def shop_edit(request, nid):
    obj = models.Shops.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = ShopsModel_edit_admin(instance=obj)
        return render(request, 'shop_edit.html', {"form": form})
    form = ShopsModel_edit_admin(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/shop/list')
    return render(request, 'shop_edit.html', {"form": form})


def shop_delete(request, nid):
    id = models.Shops.objects.filter(id=nid).first().boss_id
    models.Users.objects.filter(id=id).update(level=1)
    models.Shops.objects.filter(id=nid).delete()
    return redirect('/shop/list')


def item_list(request):
    data_dict = {}
    search_data = request.GET.get('q', "")

    if search_data:
        data_dict['id__contains'] = search_data
    items = models.Items.objects.all().filter(**data_dict)
    page_object = Pagination(request, items)
    context = {
        "search_data": search_data,
        "users": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request, 'item_list.html', context)


def item_add(request):
    if request.method == "GET":
        form = ItemsModel()
        return render(request, "item_add.html", {"form": form})
    form = ItemsModel(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect('/item/list')
    return render(request, 'item_add.html', {"form": form})


def item_edit(request, nid):
    obj = models.Items.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = ItemsModel(instance=obj)
        return render(request, 'item_edit.html', {"form": form})
    form = ItemsModel(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/item/list')
    return render(request, 'item_edit.html', {"form": form})


def item_delete(request, nid):
    models.Items.objects.filter(id=nid).delete()
    if request.session['info']['level'] == 3:
        return redirect('/item/list')
    return redirect('/shop/item/list')


def warehouse_list(request):
    data_dict = {}
    search_data = request.GET.get('q', "")

    if search_data:
        data_dict['id__contains'] = search_data
    warehouse = models.Warehouse.objects.all().filter(**data_dict)
    page_object = Pagination(request, warehouse)
    context = {
        "search_data": search_data,
        "users": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request, 'warehouse_list.html', context)


def warehouse_add(request):
    if request.method == "GET":
        form = WarehouseModel()
        return render(request, "warehouse_add.html", {"form": form})
    form = WarehouseModel(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/warehouse/list')
    return render(request, 'warehouse_add.html', {"form": form})


def warehouse_edit(request, nid):
    obj = models.Warehouse.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = WarehouseModel(instance=obj)
        return render(request, 'warehouse_edit.html', {"form": form})
    form = WarehouseModel(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/warehouse/list')
    return render(request, 'warehouse_edit.html', {"form": form})


def warehouse_delete(request, nid):
    models.Warehouse.objects.filter(id=nid).delete()
    return redirect('/warehouse/list')


def order_list(request):
    orders = models.Order.objects.all()
    page_object = Pagination(request, orders)
    context = {
        "users": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request, 'order_list.html', context)


def order_edit(request, nid):
    obj = models.Order.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = OrderModel(instance=obj)
        return render(request, 'order_edit.html', {"form": form})
    form = OrderModel(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/order/list')
    return render(request, 'order_edit.html', {"form": form})


def order_delete(request, nid):
    order = models.Order.objects.filter(id=nid).first()
    if order.status == 1:
        item = models.Items.objects.filter(id=order.iid_id).first()
        cnt = order.trade_count + item.count
        models.Items.objects.filter(id=order.iid_id).update(count=cnt)
    models.Order.objects.filter(id=nid).delete()
    if request.session['info']['level'] == 3:
        return redirect('/order/list')
    return redirect('/shop/order/list')


def shop_check_list(request):
    data_dict = {}
    search_data = request.GET.get('q', "")

    if search_data:
        data_dict['id__contains'] = search_data
    shop = models.Shops.objects.all().exclude(status=1).filter(**data_dict)
    page_object = Pagination(request, shop)
    context = {
        "search_data": search_data,
        "users": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request, 'shop_check_list.html', context)


def shop_check_edit(request, nid):
    id = models.Shops.objects.filter(id=nid).first().boss_id
    models.Shops.objects.filter(id=nid).update(status=1)
    models.Users.objects.filter(id=id).update(level=2)
    return redirect('/shop/check/list')


def shop_check_delete(request, nid):
    models.Shops.objects.filter(id=nid).delete()
    return redirect('/shop/check/list')


def item_buy(request, nid):
    obj = models.Items.objects.filter(id=nid).first()
    context = {
        "id": obj.id,
        "name": obj.name,
        "count": obj.count,
    }
    if request.method == 'GET':
        return render(request, 'item_buy.html', context)
    buy_count = int(request.POST.get("cnt"))
    if buy_count <= 0:
        context['error'] = "请输入正确的购买数量"
        context['buy_count'] = buy_count
        return render(request, 'item_buy.html', context)
    cnt = obj.count - buy_count
    if cnt < 0:
        context['error'] = "商品库存不足"
        context['buy_count'] = buy_count
        return render(request, 'item_buy.html', context)
    models.Items.objects.filter(id=nid).update(count=cnt)
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    p = obj.price * buy_count
    obj1 = models.Users.objects.filter(id=request.session['info']['id']).first()
    models.Order.objects.create(uid=obj1, iid=obj, trade_time=t, trade_count=buy_count,
                                status=1, price=p)
    return redirect('/user_home')


def user_shop_list(request):
    data_dict = {}
    search_data = request.GET.get('q', "")

    if search_data:
        data_dict['name__contains'] = search_data
    shops = models.Shops.objects.all().exclude(status=0).filter(**data_dict)
    page_object = Pagination(request, shops)
    context = {
        "search_data": search_data,
        "users": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request, 'user_shop_list.html', context)


def user_shop_item_list(request, nid):
    data_dict = {}
    search_data = request.GET.get('q', "")
    category = request.GET.get('category', '0')
    sort = request.GET.get('sort', '0')
    if search_data:
        data_dict['name__contains'] = search_data
    s = models.Shops.objects.filter(id=nid).first()
    items = models.Items.objects.all().filter(shop=s)
    items = items.filter(**data_dict)
    if category and int(category) > 0:
        items = items.filter(category=int(category))
    if sort and int(sort) == 1:
        items = items.order_by('price')
    if sort and int(sort) == 2:
        items = items.order_by('-price')
    count = items.aggregate(item_count=Count('id'))
    page_object = Pagination(request, items)
    context = {
        "search_data": search_data,
        "users": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),  # 页码
        "cate": int(category),
        "sort": int(sort),
        "count": count['item_count']
    }
    return render(request, 'user_home.html', context)


def user_order_list(request):
    user = models.Users.objects.filter(id=request.session['info']['id']).first()
    orders = models.Order.objects.all().filter(uid=user).order_by('status')
    page_object = Pagination(request, orders)
    context = {
        "users": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request, 'user_order_list.html', context)


def shop_info(request):
    user = models.Users.objects.filter(id=request.session['info']['id']).first()
    obj = models.Shops.objects.filter(boss=user).first()
    origin_boss = obj.boss.id
    if request.method == 'GET':
        form = ShopsModel_edit_user(instance=obj)
        return render(request, 'shop_info.html', {"form": form})
    form = ShopsModel_edit_user(data=request.POST, instance=obj)
    if form.is_valid():
        if form.cleaned_data['boss'].id != origin_boss:
            models.Users.objects.filter(id=origin_boss).update(level=1)
            models.Users.objects.filter(id=form.cleaned_data['boss'].id).update(level=2)
            user = models.Users.objects.filter(id=request.session['info']['id']).first()
            request.session.clear()
            request.session['info'] = {'id': user.id, 'name': user.name, 'level': user.level}
        form.save()
        return redirect('/user_home')
    return render(request, 'shop_info.html', {"form": form})


def shop_item_list(request):
    data_dict = {}
    search_data = request.GET.get('q', "")
    shop = models.Shops.objects.filter(boss_id=request.session['info']['id']).first()
    if search_data:
        data_dict['name__contains'] = search_data
    items = models.Items.objects.all().filter(shop=shop).filter(**data_dict)
    page_object = Pagination(request, items)
    context = {
        "search_data": search_data,
        "users": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request, 'shop_item_list.html', context)


def shop_item_edit(request, nid):
    obj = models.Items.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = ItemsModel(instance=obj)
        return render(request, 'shop_item_edit.html', {"form": form})
    form = ItemsModel(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/shop/item/list')
    return render(request, 'shop_item_edit.html', {"form": form})


def shop_order_list(request):
    shop = models.Shops.objects.filter(boss_id=request.session['info']['id']).first()
    items = models.Items.objects.filter(shop=shop)
    order = models.Order.objects.filter(id__isnull=True)
    for i in items:
        order = order | models.Order.objects.filter(iid=i)
    order = order.order_by('status')
    page_object = Pagination(request, order)
    context = {
        "users": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request, 'shop_order_list.html', context)


def order_send(request, nid):
    models.Order.objects.filter(id=nid).update(status=2)
    return redirect('/shop/order/list')


def user_shop_add(request):
    flag = models.Shops.objects.filter(boss_id=request.session['info']['id']).exists()
    if request.method == "GET":
        form = ShopsModel_add()
        context = {
            "flag": flag,
            "form": form
        }
        return render(request, "user_shop_add.html", context)
    form = ShopsModel_add(data=request.POST)

    if form.is_valid():
        form.save()
        id = form.cleaned_data['id']
        models.Shops.objects.filter(id=id).update(boss_id=request.session['info']['id'])
        return redirect('/user_home')
    return render(request, 'user_shop_add.html', {"form": form})


def shop_item_add(request):
    if request.method == "GET":
        form = ItemsModel()
        return render(request, "shop_item_add.html", {"form": form})
    form = ItemsModel(data=request.POST)

    if form.is_valid():
        form.save()
        shop = models.Shops.objects.filter(boss_id=request.session['info']['id']).first().id
        models.Items.objects.filter(shop__isnull=True).update(shop_id=shop)
        return redirect('/shop/item/list')
    return render(request, 'shop_item_add.html', {"form": form})

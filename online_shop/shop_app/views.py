from django.shortcuts import render, redirect
from django.contrib.auth import decorators as auth_decorators
from rest_framework import viewsets
from datetime import datetime
from . import serializers
from .models import Categories, Products, Reviews, OrdersToProducts, Orders, UserToAddress, UserAddresses, Discounts
from .permissions import ReadOnlyOrIsAdmin
from .forms import RegistrationForm
from django.db import transaction


def main(request):
    return render(
        request,
        'shop_app/main.html'
    )


def get_products(category):
    products = []
    categories = [category]
    while categories:
        category = categories.pop()
        for cat in Categories.objects.filter(supercategory=category):
            categories.append(cat)
        for product in Products.objects.filter(category=category):
            products.append(product)
    return products


def menu(request, category=None):
    context = {}
    if category:
        context["categories"] = list(Categories.objects.filter(supercategory=category))
        context['category'] = category 
        products = get_products(category)
    else:
        context["categories"] = list(Categories.objects.filter(supercategory=None))
        context['category'] = 'Все продукты'
        products = Products.objects.order_by('category')
    context['products'] = products
    context['comments'] = {obj : Reviews.objects.filter(product=obj) for obj in products}
    discounts = {}
    for product in products:
        discount_set = Discounts.objects.filter(finished__gte=datetime.now(), product=product)
        discount = None
        for discount in discount_set:
            discount = discount
            break
        if discount:
            discounts[product] = round(float(product.price) * (1 - discount.percentage/100), 2)
        
    context['discounts'] = discounts


    if request.user and request.user.is_authenticated:
        user_order = Orders.objects.filter(
            user=request.user, status='in_basket')
        if user_order:
            for order in user_order:
                order_id = order.id
                break
            basket = [Products.objects.get(
                id=product.product_id) for product in OrdersToProducts.objects.filter(order_id=order_id)]
            context['num_of_prods'] = {prod : OrdersToProducts.objects.get(order_id=order_id, product=prod).number for prod in basket}  
            print(context['num_of_prods'])
            context['basket'] = basket
            context['order_id'] = order_id
        else:
            context['basket'] = []
    return render(request, 'shop_app/menu.html', context=context)


def create_viewset(cls_model, serializer, permission):
    class ReadOnlyOrIsAdminViewSet(viewsets.ModelViewSet):
        serializer_class = serializer
        queryset = cls_model.objects.all()
        permission_classes = [permission]

    return ReadOnlyOrIsAdminViewSet


CategoryViewSet = create_viewset(
    Categories, serializers.CategorySerializer, ReadOnlyOrIsAdmin)
ProductViewSet = create_viewset(
    Products, serializers.ProductSerializer, ReadOnlyOrIsAdmin)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


@auth_decorators.login_required
def profile_page(request):
    user = request.user

    client_data = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'orders' : Orders.objects.filter(user=user)
    }
    return render(
        request,
        'shop_app/profile.html',
        context=client_data,
    )


@auth_decorators.login_required
def buy_product(request):
    product_id = request.GET['product_id']
    try:
        order_id = Orders.objects.get(user_id=request.user, status='in_basket').id
    except Exception:
        with transaction.atomic():
            order = Orders(status='in_basket', user=request.user)
            order.save()
            product = Products.objects.get(id=product_id)
            OrdersToProducts.objects.create(
                product=product, order=order, number=1)
    else:
        OrdersToProducts.objects.create(order_id=order_id, product_id=product_id, number=1)
    return redirect('menu')


def making_order(request):
    addresses = []
    for address in UserToAddress.objects.filter(user=request.user):
        addresses.append(address.address)
    return render(request, 'shop_app/make_order.html', context={'data': request.GET, 'addresses': addresses})


def cancel_order(request):
    address = UserAddresses(name=request.GET['address']) if request.GET['address'] else None
    print(type(request.GET['address']))
    order_id = UserAddresses(name=request.GET['order_id'])
    context = {}
    if address:  
        with transaction.atomic():
            address.save()
            UserToAddress.objects.create(user=request.user, address=address)
            order = Orders.objects.get(id=f'{order_id}')
            order.status = 'created'
            order.save()
            context['msg'] = 'Адрес успешно добавлен. Заказ придет на {}'.format(
                address.name)
    else:
        context['msg'] = f'Заказ {order_id} начали собирать'
        with transaction.atomic():
            order = Orders.objects.get(id=f'{order_id}')
            order.status = 'created'
            order.save()
    return render(request, 'shop_app/cancel_order.html', context=context)


def delete_product(request):
    product_id = request.GET['product_id']
    order_id = Orders.objects.get(user_id=request.user, status='in_basket').id
    OrdersToProducts.objects.filter(
        order_id=order_id, product_id=product_id).delete()
    return redirect('menu')


def filter_category(request):
    category_id = request.GET['category_id']
    category = Categories.objects.get(id=category_id)
    return menu(request, category=category)


def homepage(request):
    return render(request,
                  'shop_app/homepage.html',
                  context={
                      'count_products': Products.objects.count(),
                      'count_categories': Categories.objects.count()})

def add_comment(request):
    comment = request.GET['comment']
    product = Products.objects.get(id=request.GET['product_id'])
    Reviews.objects.create(comment=comment, user=request.user, product=product)
    return redirect('menu')

def add_num(request):
    product = Products.objects.get(id=request.GET['product_id'])
    order = Orders.objects.get(user_id=request.user, status='in_basket')
    target = OrdersToProducts.objects.get(product=product, order=order)
    target.number += 1
    target.save()
    return redirect('menu')

def del_num(request):
    product = Products.objects.get(id=request.GET['product_id'])
    order = Orders.objects.get(user_id=request.user, status='in_basket')
    target = OrdersToProducts.objects.get(product=product, order=order)
    target.number -= 1
    if target.number == 0:
        target.delete()
    else:
        target.save()
    return redirect('menu')

def show_order(request):
    order = Orders.objects.get(id=request.GET['order_id'])
    products = [orderprod.product for orderprod in OrdersToProducts.objects.filter(order=order)]
    
    return render(request, 'shop_app/show_order.html', context={'products' : products, 'order' : order})
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


@unauthenticated_user
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                name=user.username,
            )

            messages.success(request, f'Account was created for {username}')
            return redirect('login')

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_costumers = customers.count()
    total_orders = orders.count()
    delivered_orders = orders.filter(status='Delivered').count()
    pending_orders = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_orders': total_orders,
        'delivered_orders': delivered_orders,
        'pending_orders': pending_orders,
        'total_costumers': total_costumers,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def user_page(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered_orders = orders.filter(status='Delivered').count()
    pending_orders = orders.filter(status='Pending').count()
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered_orders': delivered_orders,
        'pending_orders': pending_orders,
    }
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def account_page(request):
    context = {
    }
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(pk=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()

    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
        'my_filter': my_filter,
    }
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(pk=pk)
    # form = OrderForm(initial={
    #     'customer': customer
    # })
    form_set = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        form_set = OrderFormSet(request.POST, instance=customer)
        # form = OrderForm(request.POST)
        if form_set.is_valid():
            form_set.save()
            return redirect('home')

    context = {
        'form_set': form_set,
    }
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(pk=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form': form,
    }
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(pk=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('home')

    context = {
        'order': order,
    }
    return render(request, 'accounts/delete_order.html', context)

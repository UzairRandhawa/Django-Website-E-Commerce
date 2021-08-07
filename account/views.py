from django.conf.urls import url
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.forms import fields, inlineformset_factory
from .models import *
from .forms import OrderForm
from .filter import OrderFilter
from .forms import CreateUserForm, CustomForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout

from .decorator import allowed_user, authorized_user,admin_only
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.auth.models import Group


@login_required(login_url='login')
def userPage(request):
    order = request.user.customer.order_set.all()
    ordertoatal = order.count()
    delivered = order.filter(status = 'Delivered').count()
    pending = order.filter(status = 'Pending').count()

    
    print('Order..',order)
    context = {'order':order,'ordertoatal':ordertoatal,'delivered':delivered,'pending':pending}
    return render (request , 'account/user.html',context)


@login_required(login_url='login')
@admin_only
def dashboardpage(request):
    
    customer = Customer.objects.all()
    order = Order.objects.all()

    ordertoatal = order.count()
    customertotal = customer.count()
    delivered = order.filter(status = 'Delivered').count()
    pending = order.filter(status = 'Pending').count()

    context= {'customer':customer,'order':order,
     'ordertoatal':ordertoatal,'customertotal':customertotal,'delivered':delivered,'pending':pending}
    return render (request, 'account/dashboard.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customerpage(request, pk):
    customer = Customer.objects.get(id=pk)
    order  = customer.order_set.all()
    ordercount = order.count()
    myfilter  = OrderFilter(request.GET, queryset=order)
    order = myfilter.qs
    context = {'customer': customer,'order':order, 'ordercount':ordercount,'myfilter':myfilter}
    return render (request, 'account/cutomer.html',context)


# @authorized_user
# @allowed_user(allowed_roles=['admin'])
def prodcutpage(request):
    product = Product.objects.all()
    context = {'product': product}
    return render (request, 'account/product.html',context )


# @authorized_user
# @allowed_user(allowed_roles=['admin'])
def ordercreate(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order , fields = ('product', 'status'))

    customer = Customer.objects.get(id = pk)
    formSet = OrderFormSet(instance=customer)
    if request.method == 'POST':
        # print('Submitting..', request.POST)
        # form = OrderForm(request.POST)
        formSet = OrderFormSet(request.POST, instance=customer)
        if formSet.is_valid():
            formSet.save()
            return redirect ('/')
    context = {'formSet': formSet}
    return render (request, 'account/order_form.html',context )

# @authorized_user
# @allowed_user(allowed_roles=['admin'])
def orderUpdate(request, pk):

    order = Order.objects.get(id =pk)
    formSet = OrderForm(instance=order)
    if request.method == 'POST':
        # print('Submitting..', request.POST)
        formSet = OrderForm(request.POST,instance=order)
        if formSet.is_valid():
            formSet.save()
            return redirect ('/')
    context = {'formSet': formSet}
    return render (request, 'account/order_form.html',context )

# @authorized_user
@allowed_user(allowed_roles=['admin'])
def orderDelete(request, pk):
    order = Order.objects.get(id = pk)
    if request.method == 'POST':
        order.delete()
        return redirect ('/')


    context = {'item': order}
    return render (request, 'account/delete.html',context )


def logoutpage(request):
    logout(request)
    return redirect('login')


def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username= username, password= password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username and Password does not matched.')
    context = {}
    return render(request, 'account/loginn.html', context)

def registerpage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save() 
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name= 'customer')
            user.groups.add(group)
            Customer.objects.create(
                user = user,
            )
            
            
            messages.success(request, 'Account Registered Succesfully for ' + username)
            return redirect('login')
            print('Data successfully..')

    context = {'form':form}
    return render(request, 'account/register.html', context)


def profilePage(request):
    customer = request.user.customer
    userForm = CustomForm(instance=customer)

    if request.method == 'POST':
        # print('Submitting..', request.POST)
        formSet = CustomForm(request.POST,request.FILES,instance=customer)
        if formSet.is_valid():
            formSet.save()
            
    context = {'userForm':userForm}
    return render(request, 'account/profile.html', context)
    
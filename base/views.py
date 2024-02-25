from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db  import IntegrityError
import random
from django.views.decorators.clickjacking import xframe_options_sameorigin

# Create your views here.


def login_request(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            usernames = username.replace(" ","")
            password = request.POST['password1']
            passwords = password.replace(' ','')
            user = authenticate(request, username = usernames, password = passwords)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('store:store'))
            else:
                context = {'err':'Invalid username or password'}
                return render(request, 'base/login.html', context)
        except (KeyError, Customer.DoesNotExist):
            context = {'err':'User Does Not Exist'}
            return render(request, 'base/login.html', context)
    else:

        return render(request, 'base/login.html')


def registration_request(request):
    if request.method =='POST':
        try:

            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            first_name = first_name.replace(' ','')
            last_name = last_name.replace(' ','')
            username = username.replace(' ','')
            email = email.replace(' ','')
            password1 = password1.replace(' ','')
            password2 = password2.replace(' ','')
            if password1 == password2:

                new_user = User.objects.create_user(username=username, first_name = first_name, last_name =last_name, password=password1, email= email)
                new_user.save()
                customer = Customer.objects.create(user = new_user, first_name = first_name, last_name = last_name, email = email)
                login(request, new_user)
                return HttpResponseRedirect(reverse('store:store'))
            else:
                context = {'err':'Your passwords didn\'t match'}
                return render (request, 'base/register.html', context)
        except (IntegrityError):
            context = {'err': 'A user with this username already exists.'}
            return render(request, 'base/register.html', context)
    context = {}
    return render(request, 'base/register.html', context)


def logout_request(request):
    logout(request)
    return HttpResponseRedirect(reverse('store:store'))


def store(request):
    if request.user.is_authenticated:

        products = Product.objects.all()
        customer =  Customer.objects.get(user = request.user)
        customer_cart, created = Cart.objects.get_or_create(customer = customer)
        cat = Category.objects.all()[:5]
        context = {'products': products, 'customer': customer, 'customer_cart': customer_cart, 'cat':cat}


        return render(request, 'base/store.html', context)
    else:
        products = Product.objects.all()
        cat = Category.objects.all()[:5]


        context={'products': products, 'cat':cat}
        return render(request, 'base/store.html', context)

def category(request):
    if request.user.is_authenticated:
        customer =  Customer.objects.get(user = request.user)
        customer_cart, created = Cart.objects.get_or_create(customer = customer)
        categories = Category.objects.all()
        context = {'categories': categories, 'customer':customer, 'customer_cart': customer_cart}
        return render(request, 'base/category.html', context)
    else:

        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'base/category.html', context)

def new(request):
    if request.user.is_authenticated:

        customer =  Customer.objects.get(user = request.user)
        customer_cart, created = Cart.objects.get_or_create(customer = customer)
        products = Product.objects.all().order_by('-time_added')[:20]
        context = {'products':products, 'customer':customer, 'customer_cart': customer_cart}
        return render(request, 'base/new.html', context)
    else:
        products = Product.objects.all().order_by('-time_added')[:20]
        context = {'products':products}
        return render(request, 'base/new.html', context)

def cat(request, slug):
    if request.user.is_authenticated:
        customer =  Customer.objects.get(user = request.user)
        customer_cart, created = Cart.objects.get_or_create(customer = customer)
        cat = Category.objects.get(slug = slug)
        product = Product.objects.filter(categories = cat).order_by('-time_added')
        context = {'products':product, 'cat': cat, 'customer':customer, 'customer_cart': customer_cart}
        return render(request, 'base/cat.html', context)
    else:
        cat = Category.objects.get(slug = slug)
        product = Product.objects.filter(categories = cat)
        context = {'products':product, 'cat': cat}
        return render(request, 'base/cat.html', context)

@xframe_options_sameorigin
def test(request, catslug):
    if request.user.is_authenticated:
        cat = Category.objects.get(slug = catslug)

        products = Product.objects.filter(categories = cat).order_by('-time_added')[:10]
        context = {'products':products, 'cat':cat}
        return render(request, 'base/test.html', context)
    else:

        cat = Category.objects.get(slug = catslug)

        products = Product.objects.filter(categories = cat).order_by('-time_added')[:10]
        context = {'products':products, 'cat':cat}
        return render(request, 'base/test.html', context)

@xframe_options_sameorigin
def catframe(request):
    if request.user.is_authenticated:

        cat = Category.objects.all()[:10]
        context = {'cat':cat}
        return render(request, 'base/catframe.html', context)
    else:
        cat = Category.objects.all()[:10]
        context = {'cat':cat}
        return render(request, 'base/catframe.html', context)

def product(request, catslug, prodslug):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user = request.user)
        products = Product.objects.get(slug = prodslug)

        if catslug == 'none':
            cat = products.categories.first()
        else:

            cat = Category.objects.get(slug = catslug)

        context ={'customer': customer, 'cat': cat, 'product':products}
        return render (request, 'base/product.html', context)
    else:
        products = Product.objects.get(slug = prodslug)

        if catslug == 'none':
            cat = products.categories.first()
        else:

            cat = Category.objects.get(slug = catslug)

        context ={'cat': cat, 'product':products}
        return render (request, 'base/product.html', context)
def cart(request):
    if request.user.is_authenticated:

        customer =  Customer.objects.get(user = request.user)
        customer_cart, created = Cart.objects.get_or_create(customer = customer)
        customer_cart.save()
        items = CartItem.objects.filter(cart = customer_cart)
        total = 0

        for item in items:

            price = item.item.price
            quantity = item.quantity
            item.ppi = price * quantity

            total += item.ppi
        customer_cart.total_cost = total
        customer_cart.save()


        context = {'customer': customer, 'total':total, 'items':items, 'customer_cart': customer_cart}
        return render(request, 'base/cart.html', context)
    else:
        return HttpResponseRedirect(reverse('store:login'))


def update(request, id, do):
    if request.user.is_authenticated:
        cart = Cart.objects.get(customer = Customer.objects.get(user = request.user))
        item = CartItem.objects.get(id = id)

        if do == 'up':
            item.quantity +=1
            cart.total_item += 1
        if do == 'down':
            item.quantity -=1
            cart.total_item -= 1
        item.save()
        cart.save()
        if item.quantity < 1:
            item.delete()
            return HttpResponseRedirect(reverse('store:cart'))

        return HttpResponseRedirect(reverse('store:cart'))
    else:
        return HttpResponseRedirect(reverse('store:login'))




def checkout(request):
    if request.user.is_authenticated:

        customer =  Customer.objects.get(user = request.user)
        customer_cart, created = Cart.objects.get_or_create(customer = customer)
        customer_cart.save()
        items = CartItem.objects.filter(cart = customer_cart)
        total = 0

        for item in items:

            price = item.item.price
            quantity = item.quantity
            item.ppi = price * quantity

            total += item.ppi
        shipping = ShippingInformation.objects.filter(customer = customer)


        context = {'customer': customer, 'total':total, 'shipping':shipping, 'items':items, 'customer_cart': customer_cart}
        return render(request, 'base/checkout.html', context)
    else:
        return HttpResponseRedirect(reverse('store:login'))


def add_to_cart(request, id, go, catslug):

    if request.user.is_authenticated:
        request.method == 'POST'
        customer = Customer.objects.get(user = request.user)
        customer_cart, created = Cart.objects.get_or_create(customer = customer)
        products = Product.objects.all().order_by('-time_added')
        product = Product.objects.get(id = id)
        item, created = CartItem.objects.get_or_create(cart = customer_cart, item = product)
        item.quantity += 1
        customer_cart.total_item += 1
        customer_cart.save()
        item.save()


        msg = 'WAS ADDED TO CARD'

        if go == 'prod':
            product = Product.objects.get(id = id)
            if catslug == 'none':
                cat = product.categories.first()
            else:

                cat = Category.objects.get(slug = catslug)
            

            context = {'cat':cat, 'products': products, 'product':product, 'msg':msg, 'customer': customer, 'customer_cart': customer_cart}
            return render(request, 'base/product.html', context)
        if go == 'cat':
            customer =  Customer.objects.get(user = request.user)
            customer_cart, created = Cart.objects.get_or_create(customer = customer)
            cat = Category.objects.get(slug = catslug)
            product = Product.objects.filter(categories = cat).order_by('-time_added')
            prod = Product.objects.get(id = id)
            msg = 'WAS ADDED TO CARD'
            context = {'products':product, 'prod':prod, 'cat': cat, 'customer':customer, 'customer_cart': customer_cart, 'msg':msg}

            return render(request, 'base/cat.html', context)
        if go == 'new':

            customer =  Customer.objects.get(user = request.user)
            customer_cart, created = Cart.objects.get_or_create(customer = customer)
            products = Product.objects.all().order_by('-time_added')
            prod = Product.objects.get(id = id)
            if catslug == 'none':
                cat = product.categories.first()
            msg = 'WAS ADDED TO CART'
            context = {'products':products, 'prod':prod, 'customer':customer, 'customer_cart': customer_cart, 'msg':msg}
            return render(request, 'base/new.html', context)
        else:
            customer =  Customer.objects.get(user = request.user)
            customer_cart, created = Cart.objects.get_or_create(customer = customer)
            products = Product.objects.filter(name__icontains=go)
            prod = Product.objects.get(id = id)
            if catslug == 'none':
                cat = product.categories.first()
            msg = 'WAS ADDED TO CART'
            context = {'products':products, 'prod':prod, 'customer':customer, 'customer_cart': customer_cart, 'msg':msg}
            return render(request, 'base/search.html', context)




    else:
        return HttpResponseRedirect(reverse('store:login'))

def details(request, catslug, prodslug):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user = request.user)
        customer_cart = Cart.objects.get(customer = customer)
        cat = Category.objects.get(slug = catslug)
        product = Product.objects.get(slug = prodslug)
        context = {'cat':cat, 'product':product, 'customer':customer, 'customer_cart':customer_cart}
        return render(request, 'base/details.html', context)
    else:
        return HttpResponseRedirect(reverse('store:login'))



def payment(request, tfid):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user =  request.user)
        customer_cart = Cart.objects.get(customer = customer)
        items = CartItem.objects.filter(cart = customer_cart)
        total = 0

        for item in items:

            price = item.item.price
            quantity = item.quantity
            item.ppi = price * quantity

            total += item.ppi
        ship = ShippingInformation.objects.get(id = tfid)
        order_id = random.randint(2222222222222222,9999999999999999)


        context = {'customer': customer, 'customer_cart': customer_cart, 'ship':ship, 'total': total, 'order_id':order_id}
        return render(request, 'base/payment.html', context)
    else:
        return HttpResponseRedirect(reverse('store:login'))


def order(request, tfid):
    if request.user.is_authenticated:

        customer = Customer.objects.get(user = request.user)
        cart = Cart.objects.get(customer = customer)
        items = CartItem.objects.filter(cart = cart)
        ship = ShippingInformation.objects.get(id = tfid)
        total = cart.total_cost
        details = ''
        for item in items:
            it = f'   "{str(item.quantity)}  {str(item.item.name)}"  '
            details += str(it)
        new_order = Order.objects.create(customer = customer, details =
                                        details, ship = ship, total = total )
        new_order.save()
        context = {}
        return render(request, 'base/placed.html', context)
    else:
        return HttpResponseRedirect(reverse('store:login'))

def order_test(request, ship_id):
    if request.user.is_authenticated:

        customer = Customer.objects.get(user = request.user)
        cart = Cart.objects.get(customer = customer)
        items = CartItem.objects.filter(cart = cart)
        ship = ShippingInformation.objects.get(id = ship_id)
        total = cart.total_cost
        details = ''
        status = request.GET['status']
        if status == 'successful':
            transaction_id =request.GET['transaction_id']
            tx_ref = request.GET['tx_ref']

            for item in items:
                it = f'   "{str(item.quantity)}  {str(item.item.name)}"  '
                details += str(it)
            new_order = Order.objects.create(customer = customer, details =
                                         details, ship = ship, total = total )
            new_order.save()
            return HttpResponseRedirect(reverse('store:order_status', args=(ship_id, status, transaction_id,tx_ref)))
        else:
            transaction_id=None
            status = request.GET['status']
            tx_ref = request.GET['tx_ref']


            context = {'status':status, 'tx_ref':tx_ref, 'transaction_id' : transaction_id, 'customer_cart':cart}
            return render(request, 'base/order_test.html', context)
    else:
        return HttpResponseRedirect(reverse('store:login'))

def order_status(request, ship_id, status, transaction_id, tx_ref):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user = request.user)

        customer_cart = Cart.objects.get(customer = customer)
        status = status
        transaction_id = transaction_id
        tx_ref = tx_ref

        context={'status':status, 'tx_ref':tx_ref, 'transaction_id':transaction_id, 'customer_cart' :customer_cart, 'customer':customer}
        return render(request, 'base/order_test.html', context)
    else:
        return HttpResponseRedirect(reverse('store:login'))




def create_shipping(request):
    if request.user.is_authenticated:

        request.method == "POST"
        customer = Customer.objects.get(user = request.user)

        address = request.POST['address']
        lga = request.POST['lga']
        city = request.POST['city']
        state = request.POST['state']
        number = request.POST['number']
        new_ship = ShippingInformation.objects.create(customer = customer, street = str(address), local_government_area =
                                                      str(lga), city = str(city), state = str(state), mobile = int(number))
        new_ship.save()
        return HttpResponseRedirect(reverse('store:checkout'))
    else:
        return HttpResponseRedirect(reverse('store:login'))


def change(request):
    if request.user.is_authenticated:

        request.method == 'POST'
        customer = Customer.objects.get(user = request.user)
        first = request.POST['fname']
        last = request.POST['lname']
        email = request.POST['email']
        customer.first_name = first
        customer.last_name = last
        customer.email = email
        customer.save()
        return HttpResponseRedirect(reverse('store:checkout'))
    else:
        return HttpResponseRedirect(reverse('store:login'))

def empty(request):
    if request.user.is_authenticated:

        customer = Customer.objects.get(user = request.user)
        cart = Cart.objects.get(customer = customer)
        items = CartItem.objects.filter(cart = cart)
        if None:
            pass
        else:
            cart.delete()
            return HttpResponseRedirect(reverse('store:cart'))
    else:
        return HttpResponseRedirect(reverse('store:login'))

def profile(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user = request.user)
        customer_cart = Cart.objects.get(customer = customer)
        orders = Order.objects.filter(customer = customer).order_by('-time')[:10]
        shippings = ShippingInformation.objects.filter(customer = customer)
        context = {'customer': customer, 'customer_cart':customer_cart, 'orders':orders , 'shippings':shippings}
        return render(request, 'base/profile.html', context)
    else:
        return HttpResponseRedirect(reverse('store:login'))




def search(request):
    if request.method == 'POST':

        if request.user.is_authenticated:
            customer = Customer.objects.get(user =  request.user)
            customer_cart = Cart.objects.get(customer = customer)
            search = request.POST['search']
            search = str(search)
            products = Product.objects.filter(name__icontains=search)
            cats = Category.objects.filter(name1__icontains = search)
            cats2 = Category.objects.filter(name2__icontains = search)
            context = {'customer': customer, 'customer_cart': customer_cart, 'search':search, 'products':products, 'cats': cats, 'cats2':cats2}
            return render(request, 'base/search.html', context)

        else:
            
            search = request.POST['search']
            products = Product.objects.filter(name__icontains=search)
            cats = Category.objects.filter(name1__icontains = search)
            cats2 = Category.objects.filter(name2__icontains = search)
            context = {'search':search, 'products':products, 'cats':cats, 'cats2':cats2}
            return render(request, 'base/search.html', context)
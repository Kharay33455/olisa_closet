from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db  import IntegrityError
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




def store(request):
    if request.user.is_authenticated:
            
        products = Product.objects.all()
        customer =  Customer.objects.get(user = request.user)
        customer_cart, created = Cart.objects.get_or_create(customer = customer)
        context = {'products': products, 'customer': customer, 'customer_cart': customer_cart}
        return render(request, 'base/store.html', context)
    else:
        products = Product.objects.all()


        context={'products': products}
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
    
        customer =  Customer.objects.get(user = request.user)
        customer_cart, created = Cart.objects.get_or_create(customer = customer)
        products = Product.objects.all().order_by('-time_added')
        context = {'products':products, 'customer':customer, 'customer_cart': customer_cart}
        return render(request, 'base/new.html', context)
            


def cat(request, slug):
    if request.user.is_authenticated:
        customer =  Customer.objects.get(user = request.user)
        customer_cart, created = Cart.objects.get_or_create(customer = customer)
        cat = Category.objects.get(slug = slug)
        product = Product.objects.filter(categories = cat)
        context = {'products':product, 'cat': cat, 'customer':customer, 'customer_cart': customer_cart}
        return render(request, 'base/cat.html', context)
    else:
        context = {}
        return render(request, 'base/cat.html', context)

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
    

def add_to_cart(request, id, go, catid):
    
    if request.user.is_authenticated:
        request.method == 'POST'
        customer = Customer.objects.get(user = request.user)
        customer_cart, created = Cart.objects.get_or_create(customer = customer)
        products = Product.objects.all()
        product = Product.objects.get(id = id)
        item, created = CartItem.objects.get_or_create(cart = customer_cart, item = product)
        item.quantity += 1
        customer_cart.total_item += 1
        customer_cart.save()
        item.save()


        msg = 'WAS ADDED TO CARD'

        if go == 'store':

            context = {'products': products, 'product':product, 'msg':msg, 'customer': customer, 'customer_cart': customer_cart}
            return render(request, 'base/store.html', context)
        if go == 'cat':
            customer =  Customer.objects.get(user = request.user)
            customer_cart, created = Cart.objects.get_or_create(customer = customer)
            cat = Category.objects.get(id = catid)
            product = Product.objects.filter(categories = cat)
            prod = Product.objects.get(id = id)
            msg = 'WAS ADDED TO CARD'
            context = {'products':product, 'prod':prod, 'cat': cat, 'customer':customer, 'customer_cart': customer_cart, 'msg':msg}
            
            return render(request, 'base/cat.html', context)
        if go == 'new':
            customer =  Customer.objects.get(user = request.user)
            customer_cart, created = Cart.objects.get_or_create(customer = customer)
            products = Product.objects.all().order_by('-time_added')
            prod = Product.objects.get(id = id)
            msg = 'WAS ADDED TO CART'
            context = {'products':products, 'prod':prod, 'customer':customer, 'customer_cart': customer_cart, 'msg':msg}
            return render(request, 'base/new.html', context)
            


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

        context = {'customer': customer, 'customer_cart': customer_cart, 'ship':ship, 'total': total}
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
        orders = Order.objects.filter(customer = customer).order_by('-time')
        shippings = ShippingInformation.objects.filter(customer = customer)
        context = {'customer': customer, 'customer_cart':customer_cart, 'orders':orders , 'shippings':shippings}
        return render(request, 'base/profile.html', context)
    else:
        return HttpResponseRedirect(reverse('store:login'))
    


    

def logout_request(request):
    logout(request)
    return HttpResponseRedirect(reverse('store:store'))
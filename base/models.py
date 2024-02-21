from django.db import models
from django.contrib.auth.models import User

#creating models

class Category(models.Model):
    name1 = models.CharField(max_length = 10, default = '')
    name2 = models.CharField(max_length = 10, default = '')
    slug = models.SlugField( default = '')
    background = models.ImageField(null = True, blank= True)

    def __str__(self):
        return self.slug

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    email = models.EmailField(max_length = 30)

    def __str__(self):
        """modelling bank users"""
        return f'{self.first_name} {self.last_name}| username = {self.user.username}'
    

class Product(models.Model):
    """model to handle all products"""
    name = models.CharField(max_length = 20)
    price = models.IntegerField()
    in_stock = models.BooleanField(default = True)
    picture1 = models.ImageField(null = True, blank= True)
    picture2 = models.ImageField(null=True, blank=True)
    categories = models.ManyToManyField(Category)
    time_added = models.DateTimeField(null =True, blank = True, auto_now_add = True)
    slug = models.SlugField(default = 'un-named')
    details = models.CharField(max_length = 2000, default = '')


    def __str__(self):
        #returns name of product on default
        return self.name
    
class Cart(models.Model):
    """model the cart"""
    customer = models.OneToOneField(Customer, on_delete = models.CASCADE)
    total_item = models.IntegerField(default = 0)
    total_cost = models.IntegerField(default = 0)

    def __str__(self):
        return f'{self.customer.first_name.title()}\'s  cart'
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, null = True, blank = True)
    item = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 0)

    def __str__(self):
        quantity = self.quantity
        quantity = str(quantity)
        return f'{quantity + " " + self.item.name}'
    
class ShippingInformation(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    street = models.CharField(max_length = 30)
    local_government_area = models.CharField(max_length = 30)
    city = models.CharField(max_length = 10)
    state = models.CharField(max_length = 10)
    mobile = models.IntegerField(null = True, blank = True)

    def __str__(self):
        return f"{self.customer.first_name}'s {self.city} shipping adress "
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    details = models.CharField(max_length = 100, default = '')
    ship = models.ForeignKey(ShippingInformation, on_delete = models.SET_NULL, null = True)
    time = models.DateTimeField(auto_now_add = True)
    total = models.IntegerField(default = 0)
    completed = models.BooleanField(default =  False)


    def __str__(self):
        return f'Order for {self.customer.first_name} on {str(self.time)}' 
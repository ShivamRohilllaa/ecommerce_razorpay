from django.db import models
from autoslug import AutoSlugField
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    desc = models.TextField(blank=True)
    image = models.ImageField(upload_to='category', blank=True)

    class Meta:
        ordering = ('name',) 
        verbose_name = ('category') 
        verbose_name_plural = ('categories') 

    def get_url(self):
        return reverse('product_by_category', args=[self.slug]) 

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)        
    slug = AutoSlugField(populate_from='name', unique=True)        
    desc = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)        
    price = models.DecimalField(max_digits=10, decimal_places=2)        
    image = models.ImageField(upload_to='products')        
    image1 = models.ImageField(upload_to='products')        
    image2 = models.ImageField(upload_to='products')        
    image3 = models.ImageField(upload_to='products')        
    image4 = models.ImageField(upload_to='products')        
    stock = models.IntegerField()        
    available = models.BooleanField(default=True)        
    created = models.DateTimeField(auto_now_add=True)        
    updated = models.DateTimeField(auto_now_add=True)        

    class Meta:
        ordering = ('name',) 
        verbose_name = ('product') 
        verbose_name_plural = ('products')

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])       

    def __str__(self):
        return self.name
         
class Cart(models.Model):
    cart_id = models.CharField(max_length=500, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='Cart'
        ordering = ['date_added']

    def __str__(self):
        return self.cart_id
        
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)        
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table='CartItem'

    def sub_total(self):
        return self.product.price*self.quantity

    def __str__(self):
        return self.product.name
            

class Order(models.Model):
    token = models.CharField(max_length=250, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='INR ORDER TOTAL')
    emailAddress = models.EmailField(max_length=250, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    billingName = models.CharField(max_length=250, blank=True)    
    billingAddress1 = models.CharField(max_length=250, blank=True)    
    billingCity = models.CharField(max_length=250, blank=True)    
    billingPostcode = models.CharField(max_length=250, blank=True)    
    billingCountry = models.CharField(max_length=250, blank=True)        
    shippingName = models.CharField(max_length=250, blank=True)    
    shippingAddress1 = models.CharField(max_length=250, blank=True)    
    shippingCity = models.CharField(max_length=250, blank=True)    
    shippingPostcode = models.CharField(max_length=250, blank=True)    
    shippingCountry = models.CharField(max_length=250, blank=True)  
    items_json = models.CharField(max_length=5000)
    razorpayid = models.CharField(max_length=255,default="")
    razorpaypaymentid = models.CharField(max_length=255,default="")
    razorpaysignature = models.CharField(max_length=255, default="")  

    class Meta:
        db_table='Order'
        ordering = ['-created']

    def __str__(self):
        return str(self.id)

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."

class OrderItem(models.Model):
    product = models.CharField(max_length=250, blank=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='INR Price')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        db_table = 'OrderItem'

    def __str__(self):
        return str(self.order)
                
        


    

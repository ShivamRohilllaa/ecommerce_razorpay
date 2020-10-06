from django.shortcuts import render, get_object_or_404, redirect
from .models import * 
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt  
import json
import razorpay
client = razorpay.Client(auth =("rzp_test_KWUdrmCKETqTCk", "pyjF8WkHpZvZZWEBZPqjgVv8"))

# Create your views here.

def home(request):
    products = Product.objects.filter(available=True)
    context={'products': products}
    return render(request, 'index.html',context)


def product_by_category(request, category_slug=None):
    category_page = None
    products = None
    if category_slug != None:
        category_page = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category_page, available=True)

    else:
        products = Product.objects.all().filter(available=True)
    
    context={'category': category_page, 'products': products}
    return render(request, 'products.html',context)


def product_page(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'product_details.html', {'product': product})


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id = _cart_id(request))

    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()    
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()
    return redirect('cart_detail') 

def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    # stripe.api_key = settings.STRIPE_SECRET_KEY
 
    if request.method == 'POST':
        total = int(total)
        description = 'JNJ Jewellers'
        data_key = 'rzp_test_KWUdrmCKETqTCk'      
        # emailAddress = request.POST.get("emailAddress")
        billingName = request.POST.get("billingName")
        billingAddress1 = request.POST.get("billingAddress1")
        billingCity = request.POST.get("billingCity")
        billingPostcode = request.POST.get("billingPostcode")
        billingCountry = request.POST.get("billingAddressCountry")
        shippingName = request.POST.get("shippingName")
        shippingAddress1 = request.POST.get("shippingAddress1")
        shippingCity = request.POST.get("shippingCity")
        shippingPostcode = request.POST.get("shippingPostcode")
        shippingCountry = request.POST.get("shippingAddressCountry")    
        order_receipt = 'order_rcptid_11'           
        razorpay_order = client.order.create({'amount':total, 'currency':'INR', 'payment_capture':'1','receipt':order_receipt})
        print(razorpay_order['id'])    
        order_details = Order(billingName=billingName, billingAddress1=billingAddress1,billingCity=billingCity,billingPostcode=billingPostcode,billingCountry=billingCountry,shippingName=shippingName,shippingAddress1=shippingAddress1,shippingCity=shippingCity, shippingPostcode=shippingPostcode,shippingCountry=shippingCountry, razorpayid=razorpay_order['id'],total=total)
        order_details.save()
        for order_item in cart_items:
            or_item = OrderItem.objects.create(product=order_item.product.name, quantity=order_item.quantity, price=order_item.product.price)
            or_item.save()            
        products = Product.objects.get(id=order_item.product.id)
        products.stock = int(order_item.product.stock - order_item.quantity)
        products.save()
        order_item.delete
        # print a message when the order is created
        print('the order has been created')
        context = {'cart_items':cart_items, 'total':total, 'counter':counter, 'description':description, 'data_key':data_key, 'order_id': razorpay_order['id']}
        return render(request, 'cart.html', context)    
        # return redirect('thanks', order_details.id)

    context = {'cart_items':cart_items, 'total':total, 'counter':counter}
    return render(request, 'cart.html', context)

def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    else:
        cart_item.delete()

    return redirect('cart_detail')        

def cart_delete(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart_detail')        

@csrf_exempt
def thank_page(request, order_id):
    if order_id:
        customer_order = get_object_or_404(Order, id=order_id)
    coontext = {'customer_order':customer_order}
    return render(request, 'thankyou.html') 

def app_charge(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            token = request.POST.get('razorpay_order_id','')
            signature = request.POST.get('razorpay_signature','')
            params_dict = { 
            'razorpay_order_id': token, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }
            order_db = Order.objects.get(razorpayid=token)
            order_db.razorpaypaymentid = payment_id
            order_db.razorpaysignature = signature
            order_db.save()
            result = razorpay.Client.utility.verify_payment_signature(params_dict)
            print(result)
            if result==None:
                amount = order_db.amount
                try:
                    razorpay.Client.payment.capture(payment_id, amount)
                    update = OrderUpdate(token=order_db.token, update_desc="The order has been placed")
                    update.save()
                    thank = True
                    id = request.POST.get('shopping_order_id','')
                    params = {'thank': thank, 'id': id}
                    # response = json.dumps(razorpay_client.payment.fetch(payment_id))
                    return render(request, 'shop/thankyou.html', params)
                except:
                    update = OrderUpdate(token=order_db.token, update_desc="Payment is unsuccessful")
                    update.save()
                    thank =  False
                    return render(request, 'shop/thankyou.html', {'thank': thank})
            else:
                update = OrderUpdate(token=order_db.token, update_desc="Payment is unsuccessful")
                update.save()
                thank =  False
                return render(request, 'shop/thankyou.html', {'thank': thank})
        except:
            update = OrderUpdate(token=order_db.token, update_desc="Payment is unsuccessful")
            update.save()
            thank =  False
            return render(request, 'shop/thankyou.html', {'thank': thank})







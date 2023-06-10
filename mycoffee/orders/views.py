from django.shortcuts import render , redirect
from django.contrib import messages
from products.models import Product
from .models import Order, Order_Details
from django.utils import timezone



def add_to_cart(request):

    if 'pro_id' in request.GET and 'qty' in request.GET and 'price' in request.GET and request.user.is_authenticated and not request.user.is_anonymous:
        pro_id = request.GET['pro_id']
        qty = request.GET['qty']
        order = Order.objects.all().filter(user=request.user, is_finished=False)

        if not Product.objects.all().filter(id=pro_id).exists():
            return redirect('products')

        pro = Product.objects.get(id=pro_id)

        if order:
            #messages.success(request,'يوجد طلب قديم')
            old_order = Order.objects.get(user=request.user,is_finished=False)
            orderdetails = Order_Details.objects.create(product=pro,order=old_order,price=pro.price,quantity=qty)
            messages.success(request,'was added to cart for old order')
        else:
            #messages.success(request,'سوف يتم عمل طلب جديد')
            new_order = Order()
            new_order.user = request.user
            new_order.order_date = timezone.now()
            new_order.is_finished = False
            new_order.save()
            orderdetails = Order_Details.objects.create(product=pro,order=new_order,price=pro.price,quantity=qty)
            messages.success(request,'was added to cart for new order')
        return redirect('/products/' + request.GET['pro_id'])
    else:
        
        return redirect('products')


def cart(request):

    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user,is_finished=False):
            order = Order.objects.get(user=request.user,is_finished=False)
            orderdetails = Order_Details.objects.all().filter(order=order)
            total = 0
            for sub in orderdetails:
                total += sub.price * sub.quantity
            context = {
                'order':order,
                'orderdetails':orderdetails,
                'total':total
            }

    return render(request,'orders/cart.html',context)

    

from django.shortcuts import get_object_or_404 , render
from django.http import HttpResponse
from .models import Product

# Create your views here.

def products(request):

    pro = Product.objects.all()
    name = ''
    description = ''
    p_from = None
    p_to = None
    cs = None

    # to get values from query string

    if 'cs' in request.GET:
        cs = request.GET['cs']
        if not cs:
            cs = 'off'

    if 'searchname' in request.GET :
        name = request.GET['searchname']
        if name:
            if cs == 'on':
                pro = pro.filter(name__contains=name)
            else:
                pro = pro.filter(name__icontains=name)

            

    if 'searchdesc' in request.GET :
        description = request.GET['searchdesc']
        if description:
            if cs == 'on':
                pro = pro.filter(description__contains=description)
            else:
                pro = pro.filter(description__icontains=description)

            

    if 'searchpricefrom' in request.GET and 'searchpriceto' in request.GET:
        p_from = request.GET['searchpricefrom']
        p_to = request.GET['searchpriceto']

        if p_from and p_to:
            if p_from.isdigit() and p_to.isdigit():
                pro = pro.filter(price__gte=p_from , price__lte=p_to)    #gte means >=   lte means <=

    context = {
        'products':pro
    }
    return render(request , 'products/products.html' , context)

def product(request , pro_id):
    context = {
        'product':get_object_or_404(Product, pk=pro_id)
    }
    return render(request , 'products/product.html' , context)

def search(request):
    return render(request , 'products/search.html')



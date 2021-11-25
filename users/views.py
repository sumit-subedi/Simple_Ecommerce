from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Cart, SliderImage, Category, Product,  order, ordered_item
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages


# Create your views here.
@login_required(login_url='/accounts/login') 
def index(request):
    sliderimage = SliderImage.objects.all()
    products = Product.objects.all()
    
    context = {
        'sliderimage': sliderimage,
        'categories' : Category.objects.all(),
        'products' :products
    }
    return render (request, 'index.html', context)

@login_required(login_url='/accounts/login') 
def search(request):

    query = request.GET['search']

    
    try:
        q1, q2 = query.split(' ')
    except(ValueError ):
        if len(query) >4:
            q1, q2 = query[0: int(len(query)/2)], query[int(len(query)/2) : ]
        else:
            q1, q2 = query, query
    products = Product.objects.filter(Q(name__icontains=query)  | Q(category__name__icontains=query) | Q(name__icontains=q1)  | Q(category__name__icontains=q1)
    | Q(name__icontains=q2)  | Q(category__name__icontains=q2)).order_by('id')
    paginator = Paginator(products, 10)
    
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)         

    context = {
        'products':products,
        'query': query
    }
    return render (request, 'search.html', context)

@login_required(login_url='/accounts/login') 
def product_details(request, pk):
    product = Product.objects.get(id = pk)
    
    context = {
        'product' : product, 
    }

    return render (request, 'product-detail.html', context)

@login_required(login_url='/accounts/login') 
def addtocart(request, pk):
    if request.method == 'POST':
        product = Product.objects.get(id = pk)
        if Cart.objects.filter(user = request.user, item = product).exists():
            print('here')
            messages.error(request, 'Item already in cart.')
            # messages.add_message(request, messages.INFO, 'Signout Successful.')
            return redirect(request.POST['path'])
        cart = Cart(user = request.user, item = product, quantity = request.POST['quantity'])
        cart.save()
        messages.success(request, 'Item successfully added to the cart')
        return redirect(request.POST['path'])
    
    cartitem = Cart.objects.get(id = pk)
    cartitem.quantity = int(request.GET['quantity'])
    cartitem.save()
    products = Cart.objects.filter(user = request.user)
    sum = 0
    for product in products:
        sum += (product.item.with_discount_price) * product.quantity
    context = {
        'product': cartitem,
        'sum': sum
    }
    return redirect('/cart')

@login_required(login_url='/accounts/login') 
def cart(request):
    products = Cart.objects.filter(user = request.user)
    sum = 0
    for product in products:
        sum += (product.item.with_discount_price) * product.quantity
    context = {
        'products': products,
        'sum': sum
    }
    return render(request, 'cart.html', context)

@login_required(login_url='/accounts/login') 
def confirmOrder(request):
    if request.method == 'GET':
        products = Cart.objects.filter(user = request.user)
        sum = 0
        if len(products) == 0:
            messages.info(request,'Order cannot be placed')
            return redirect( 'cart')
        for product in products:
            sum += (product.item.with_discount_price) * product.quantity
        context = {
            'products': products,
            'sum' : sum
        }
        return render(request, 'confirmorder.html', context)
    if request.method == 'POST':
        cartitems = Cart.objects.filter(user = request.user)
        orderobj = order(user = request.user, order_address = request.POST['address'],
                    delivery_name = request.POST['name'], delivery_phone = request.POST['phone'])
        orderobj.save()
        for item in cartitems:
            orderitem = ordered_item(order = orderobj, item = item.item,
                        itemname = item.item.name, quantity = item.quantity, price = item.item.with_discount_price)
            orderitem.save()
            item.delete()
        return redirect ('home')


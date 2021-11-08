from django.shortcuts import render
from .models import SliderImage, Category, Product
# Create your views here.

def index(request):
    sliderimage = SliderImage.objects.all()
    products = Product.objects.all()
    
    context = {
        'sliderimage': sliderimage,
        'categories' : Category.objects.all(),
        'products' :products
    }
    return render (request, 'index.html', context)
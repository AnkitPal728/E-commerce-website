from django.http import HttpResponse
from django.shortcuts import render
from . models import Product, Contact
from math import ceil

# Create your views here.
def index(request):
    allprods = []
    allcats = Product.objects.values('pro_category', 'id')
    cats = {item['pro_category'] for item in allcats}
    for cat in cats:
        prods = Product.objects.filter(pro_category = cat)
        n = len(prods)
        nslides = n//4 + ceil((n/4) - (n//4))
        allprods.append([prods, range(0, nslides), nslides])
    params = {'allprods': allprods}
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/about.html')

def tracker(request):
    return render(request, 'shop/tracker.html')

def checkout(request):
    return render(request, 'shop/checkout.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('Name', "")
        email = request.POST.get('Email', "")
        mobile = request.POST.get('Mobile', "")
        desc = request.POST.get('desc', "")
        contact = Contact(cus_name=name, cus_email=email, cus_mobile=mobile, desc=desc)
        contact.save()
    return render(request, 'shop/contact.html')

def prodview(request, myid):
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodview.html', {'product': product[0]})
from django.http import HttpResponse
from django.shortcuts import render
from . models import Product, Contact, Order, OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from payTm import Checksum
# Create your views here.
MERCHANT_KEY = 'YD8MC4RrXoaqGdn6'


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

def searchMatch(query, item):
    query = query.lower()
    if query in item.desc.lower() or query in item.pro_name.lower() or query in item.pro_category.lower() or query in item.pro_subcategory.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allprods = []
    val = False
    allcats = Product.objects.values('pro_category', 'id')
    cats = {item['pro_category'] for item in allcats}
    for cat in cats:
        prod = Product.objects.filter(pro_category = cat)
        prods = [item for item in prod if searchMatch(query, item)]
        n = len(prods)
        nslides = n//4 + ceil((n/4) - (n//4))
        if n != 0:
            allprods.append([prods, range(0, nslides), nslides])
    if len(allprods) == 0:
        val = True
    params = {'allprods': allprods, 'true': val}
    return render(request, 'shop/search.html', params)

def about(request):
    return render(request, 'shop/about.html')

def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(o_id=orderId, o_email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    updates = json.dumps([updates, order[0].o_json], default=str)
                    return HttpResponse(updates)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')

def checkout(request):
    if request.method == "POST":
        json_item = request.POST.get('json_item', "")
        amount = request.POST.get('amount', "")
        name = request.POST.get('name', "")
        email = request.POST.get('email', "")
        mobile = request.POST.get('mobile', "")
        address1 = request.POST.get('address1', "")
        address2 = request.POST.get('address2', "")
        state = request.POST.get('state', "")
        city = request.POST.get('city', "")
        zip_c = request.POST.get('zip_c', "")
        order = Order(o_json=json_item, o_amount=amount, o_name=name, o_email=email, o_mobile=mobile, o_add1=address1, o_add2=address2, o_state=state, o_city=city, o_zip=zip_c)
        order.save()
        update = OrderUpdate(order_id=order.o_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.o_id
        #return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
        # request paytm to transfer the amount to your account after payment by user
        param_dict = {

            'MID': 'JPzDem84539034781155',
            'ORDER_ID': str(order.o_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/payTmhandler/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})
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

@csrf_exempt
def payTmhandler(request):
    #paytm sends to you request
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})

from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json

def index(request):
  
    allProds = []
    category_products = Product.objects.values('category', 'id')
    cats = {item['category'] for item in category_products}
    for cat in cats:
        products = Product.objects.filter(category=cat)
        n = len(products)
        number_slide = n // 4 + ceil((4 / n) - (4 // n))
        allProds.append([products, range(1, number_slide), number_slide])
    params = {'allProds': allProds}
    return render(request, 'index.html', params)


def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:    
        return False


def search(request):
    query = request.GET.get('search')
    allProds = []
    category_products = Product.objects.values('category', 'id')
    cats = {item['category'] for item in category_products}
    for cat in cats:
        products_temp = Product.objects.filter(category=cat)
        products = [item for item in products_temp if searchMatch(query, item)]
        n = len(products)
        number_slide = n // 4 + ceil((n / 4) - (n // 4))
        if len(products) != 0:
            allProds.append([products, range(1, number_slide), number_slide])
            
    params = {'allProds': allProds, 'msg':""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter the relevent search Query"}
    return render(request, 'index.html', params)


def about(request):
    return render(request, 'about.html')

def product(request):
    return render(request, 'productviews.html')


def contact(request):
    send = False
    if request.method == "POST":
        contact_us = request.POST.get('contact_us', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        description = request.POST.get('description', '')
        contact = Contact(contact_us=contact_us, name=name, email=email, phone=phone, description=description)
        contact.save()
        send = True
        return render(request, 'contact.html', {'send': send})

    return render(request, 'contact.html')


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_description, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates":updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"NoItems"}')
        except Exception as e:
            return HttpResponse('{"status":"Error"}')

    return render(request, 'tracker.html')


def productviews(request, myid):
    product = Product.objects.filter(id=myid)
    return render(request, 'productviews.html', {'product': product[0]})


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('items_json', '')
        name = request.POST.get('fname', '') + " " + request.POST.get('lname', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('add1', '') + " " + request.POST.get('add2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        order = Order(items_json=items_json, name=name, amount=amount, email=email, phone=phone, address=address, city=city, state=state, zip_code=zip_code, )
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_description="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'checkout.html', {'thank': thank, 'id': id})

    return render(request, 'checkout.html')

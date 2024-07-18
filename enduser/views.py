from datetime import datetime
from http.client import responses
import json
from django.shortcuts import render
from django.http import HttpResponse
from enduser import models

# Create your views here.

#Home Page
def index(request):
    return render(request,'index.html')

#Products Page
def Products(request):
    queryset = models.Products.objects.all()
    return render(request, 'product.html', {'products': queryset})

#Cart Page
def ShoppingCart(request):
    return render(request,'cart.html')

#About Us 
def about(request):
    return render(request,'about.html')

#checkout
def checkout(request):
    return render(request,'checkout.html')

#login
def login(request):
    return render(request,'login.html')

#contact
def contact(request):
    return render(request,'contact.html')

#order
def order(request):
    if request.method == 'POST':
        return render(request,'order.html')
    else:
       return index(request)


#checkout
def ordercomplete(request):
    if(request.method=='POST'):
        shopping_list = request.POST.get('shopping_list')
        billingemail = request.POST.get('billing-email')
        name = request.POST.get('billing-name')
        addr = request.POST.get('billing-addr')
        zip = request.POST.get('billing-zip')
        city = request.POST.get('billing-city')
        country = request.POST.get('billing-country')
        cost = request.POST.get('shipping-cost')
        card = request.POST.get('card_number')
        expdate = request.POST.get('expiration_date')
        cvc = request.POST.get('cvc')
        
        cartitems = json.loads(shopping_list)

        cus = models.Customers.objects.filter(email=billingemail).first()
        cusno=0
        totalprice=0
        noitems=0
        newinvoice =None
        customer=None
        if (cus is None):
            newcustomer= models.Customers(name=name,lastname=name,cellno=0,email=billingemail)
            models.Customers.save(newcustomer)
            cusno = newcustomer.customerno
            customer = newcustomer
        else:
            cusno = cus.customerno
            customer = cus
        
        newinvoice = models.Invoices(invoicesamt=0,invoicesqty=0,invoicesdate=datetime.today(),invoicestype=0,invoicesfor=customer)
        
        models.Invoices.save(newinvoice)    
        

        newcart = models.Cart(cartqty=0,cartprice=0,invoice=newinvoice,cartstate=0,customerno=customer)

        models.Cart.save(newcart)

        for item in cartitems['items']:
            prod = models.Products.objects.get(idproducts=int(item['prodid']))
            newcartitem = models.Cartitems(cart=newcart,product=prod)
            totalprice +=item['price']
            noitems +=item['qty']
            models.Cartitems.save(newcartitem)

        newinvoice.invoicesamt=totalprice
        newinvoice.invoicesqty=noitems
        newinvoice.save()

        newcart.cartprice=totalprice
        newcart.cartqty=noitems
        newcart.save()

    return render(request,'completed.html',{'invoiceno': newinvoice.idinvoices})
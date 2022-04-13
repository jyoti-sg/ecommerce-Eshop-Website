from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from . import models
from . import forms
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test

# Home view
def homeview(request):
    products=models.Product.objects.all()
    #for count product in cart
    if 'product_ids' in request.COOKIES:
        product_ids=request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    # user need to login
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    context={'products':products,'product_count_in_cart':product_count_in_cart}
    return render(request,'ecom/index.html',context)

# serch view for search any item
def search_view(request):
    query=request.GET['query']
    products=models.Product.objects.all().filter(name__icontains=query)
    context={'products':products}
    return render(request,"ecom/index.html",context)


# view product to show Product in detail
def view_product(request,pid):
    products=models.Product.objects.all().filter(id=pid)[0]
    #for count product in cart
    if 'product_ids' in request.COOKIES:
        product_ids=request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    context={'products':products,'product_count_in_cart':product_count_in_cart}

    return render(request,"ecom/product_detail.html",context)



#for sign up
def customer_signup(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    if request.method=='POST':
         userForm=forms.CustomerUserForm(request.POST)
         customerForm=forms.CustomerForm(request.POST,request.FILES)
         if userForm.is_valid() and customerForm.is_valid():
             user=userForm.save()
             user.set_password(user.password)
             user.save()
             customer=customerForm.save(commit=False)
             customer.user=user
             customer.save()
             my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
             my_customer_group[0].user_set.add(user)
         return HttpResponseRedirect('/customerlogin/')

    context={'userForm':userForm,'customerForm':customerForm}
    return render(request,'ecom/customersignup.html',context)

#after login
def afterlogin_view(request):
    return redirect('customer-home')
@login_required(login_url='customerlogin')

# customer home view
def customerhome_view(request):
    products=models.Product.objects.all()
    ##for count product in cart
    if 'products_ids' in request.COOKIES:
        product_ids=request.COOKIES['product_ids']
        counter=product_ids.split("|")
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    context={'products':products,'product_count_in_cart':product_count_in_cart}
    return render(request,'ecom/customer_home.html',context)



#Add To Cart view
def add_to_cart_view(request,pk):
    products=models.Product.objects.all()

    #for cart counter,fetching product added by customer from cookies
    if 'product_ids' in request.COOKIES:
        product_ids=request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    context={'products':products,'product_count_in_cart':product_count_in_cart}
    response=render(request,"ecom/customer_home.html",context)

    #create cookie and add product_ids in cookie
    if 'product_ids' in request.COOKIES:
        product_ids=request.COOKIES['product_ids']
        if product_ids=="":
            product_ids=str(pk)
        else:
            product_ids=product_ids+"|"+str(pk)
        response.set_cookie('product_ids',product_ids)
    else:
        response.set_cookie('product_ids', pk)
    product=models.Product.objects.get(id=pk)
    return response


#view items in cart
def cart_view(request):
    #for cart counter,fetching product added by customer from cookies
    if 'product_ids' in request.COOKIES:
        product_ids=request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0



    #fetching product details from db whose id present in cookie
    products=None
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids=request.COOKIES['product_ids']
        if product_ids != "":
            product_id_in_cart=product_ids.split('|')
            products= models.Product.objects.all().filter(id__in =product_id_in_cart)
        #for toatal Price showm in cart
            for p in products:
                total=total+p.price
    context={'products':products,'product_count_in_cart':product_count_in_cart,'total':total}
    return render(request,'ecom/cart.html',context)


#remove items from cart
def remove_from_cart_view(request,pk):
    #for cart counter
    if 'product_ids' in request.COOKIES:
        product_ids=request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    #remove Product from cookie
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids=request.COOKIES['product_ids']

        product_id_in_cart=product_ids.split('|')
        product_id_in_cart=list(set(product_id_in_cart))
        product_id_in_cart.remove(str(pk))
        products= models.Product.objects.all().filter(id__in =product_id_in_cart)
        #for toatal Price showm in cart after removing a item from cart
        for p in products:
            total=total+p.price
        #for update cookie value after removing a item in from cart_view
        value=""
        for i in range(len(product_id_in_cart)):
            if i==0:
                value=value+product_id_in_cart[0]
            else:
                value=value+"|"+product_id_in_cart[i]

        #context={'products':products,'product_count_in_cart':product_count_in_cart,'total':total}
        #return render(request,'ecom/cart.html',context)
        response=render(request,"ecom/cart.html",{'products':products,'total':total,'product_count_in_cart':product_count_in_cart})
        if value=="":
            response.delete_cookie('product_ids')
        response.set_cookie('product_ids',value)
        return response


# customer address view
@login_required(login_url='customerlogin')
def customer_address_view(request):
    # this is for checking whether product is present in cart or not
    # if there is no product in cart we will not show address form
    product_in_cart=False
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_in_cart=True
    #for counter in cart
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    addressForm = forms.AddressForm()
    if request.method == 'POST':
        addressForm = forms.AddressForm(request.POST)
        if addressForm.is_valid():
            # here we are taking address, email, mobile at time of order placement
            # we are not taking it from customer account table because
            # these thing can be changes
            email = addressForm.cleaned_data['Email']
            mobile=addressForm.cleaned_data['Mobile']
            address = addressForm.cleaned_data['Address']
            #for showing total price on payment page.....accessing id from cookies then fetching  price of product from db
            total=0
            if 'product_ids' in request.COOKIES:
                product_ids = request.COOKIES['product_ids']
                if product_ids != "":
                    product_id_in_cart=product_ids.split('|')
                    products=models.Product.objects.all().filter(id__in = product_id_in_cart)
                    for p in products:
                        total=total+p.price

            response = render(request, 'ecom/payment.html',{'total':total})
            response.set_cookie('email',email)
            response.set_cookie('mobile',mobile)
            response.set_cookie('address',address)
            return response
    return render(request,'ecom/customer_address.html',{'addressForm':addressForm,'product_in_cart':product_in_cart,'product_count_in_cart':product_count_in_cart})


#payment success view
@login_required(login_url='customerlogin')
def payment_success_view(request):
    # Here we will place order | after successful payment
    # we will fetch customer  mobile, address, Email
    # we will fetch product id from cookies then respective details from db
    # then we will create order objects and store in db
    # after that we will delete cookies because after order placed...cart should be empty
    customer=models.Customer.objects.get( user_id = request.user.id )
    products=None
    email=None
    mobile=None
    address=None
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_id_in_cart=product_ids.split('|')
            products=models.Product.objects.all().filter(id__in = product_id_in_cart)
            # Here we get products list that will be ordered by one customer at a time

    # these things can be change so accessing at the time of order...
    if 'email' in request.COOKIES:
        email=request.COOKIES['email']
    if 'mobile' in request.COOKIES:
        mobile=request.COOKIES['mobile']
    if 'address' in request.COOKIES:
        address=request.COOKIES['address']

    # here we are placing number of orders as much there is a products
    # suppose if we have 5 items in cart and we place order....so 5 rows will be created in orders table
    # there will be lot of redundant data in orders table...but its become more complicated if we normalize it
    for product in products:
        models.Order.objects.get_or_create(customer=customer,product=product,status='Pending',email=email,mobile=mobile,address=address)

    # after order placed cookies should be deleted
    response = render(request,'ecom/payment_success.html')
    response.delete_cookie('product_ids')
    response.delete_cookie('email')
    response.delete_cookie('mobile')
    response.delete_cookie('address')
    return response



#logout view
@login_required(login_url='customerlogin')
def my_order_view(request):
    customer=models.Customer.objects.get( user_id = request.user.id )
    orders=models.Order.objects.all().filter( customer_id = customer )
    ordered_products=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_products.append(ordered_product)
    return render(request,'ecom/my_order.html',{'data':zip(ordered_products,orders)})


#customer profile
@login_required(login_url='customerlogin')
@user_passes_test('is_customer')
def my_profile_view(request):
    customer=models.Customer.objects.get( user_id = request.user.id )
    return render(request,'ecom/my_profile.html',{'customer':customer})


def send_feedback_view(request):
    feedbackForm=forms.FeedbackForm()
    if request.method == 'POST':
        feedbackForm = forms.FeedbackForm(request.POST)
        if feedbackForm.is_valid():
            feedbackForm.save()
            return render(request, 'ecom/feedback_sent.html')
    return render(request, 'ecom/send_feedback.html', {'feedbackForm':feedbackForm})
def contactus_view(request):
    return render(request,'ecom/contact_us.html')

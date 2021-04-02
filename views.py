from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.models.customer import Customer
from store.models.category import Category
from store.models.product import Product
from store.models.orders import Order
from django.contrib.auth.hashers import make_password,check_password
from django.views import View
#from .decorators import customer_user
from django.contrib.auth.decorators import login_required

# Create your views here.

# class based view for signupview
class SingnupView(View):
    def get(self, request):
        return render(request, "signup.html")
    
    def post(self, request):
        #  post data from user
        postData = request.POST
        first_name = postData.get("firstname")
        last_name = postData.get("lastname")
        phone_no = postData.get("phone")
        email = postData.get("email")
        password = postData.get("password")

        value = {
                "first_name":first_name,
                "last_name": last_name,
                "phone_no":phone_no,
                "email":email
            }
        customer = Customer(first_name=first_name, last_name=last_name, phone_no=phone_no, email=email, password=password)
        
        error_message = self.ValidateCustomer(customer) # ValidateCustomer method calls here instance method

        # saving
        if(not error_message):
            customer.password = make_password(customer.password) # for password hashing
            customer.save()
            #customer.register()  #(by using instance method we create in customer model to save the data)
            return redirect("login")
        else:
            data = {
                "values":value,
                "error":error_message
            }
            return render(request,"signup.html",data)

    def ValidateCustomer(self,customer):
        # validation 
        error_message = None
        if (not customer.first_name):
            error_message = "First Name Required"
        elif len(customer.first_name)<2:
            error_message = "first_name should be more than 2 char"
        elif (not customer.last_name):
            error_message = "Last name required"
        elif len(customer.last_name)<2:
            error_message = "last_name should be more than 4 char"
        elif (not customer.phone_no):
            error_message = "Phone Number required"
        elif len(customer.phone_no)<9:
            error_message = "Enter valid Mobile number"
        elif (not customer.email):
            error_message = "Email required"
        elif (not customer.password):
            error_message = "password requird"
        elif customer.isExist():
            error_message = "Email already Exist"
        
        return error_message


# class based login view
class loginView(View):
    def get(self,request):
        return render(request,"login.html")
    def post(self,request):
        email1 = request.POST.get("email")
        password1 = request.POST.get("password")
        customer = Customer.get_customer_by_email(email1)
        error_message = None
        if customer:
            flag = check_password(password1,customer.password)
            #print(flag)  --- True
            if flag:
                request.session["customer"] = customer.id
                return redirect('homepage')
            else:
                error_message = "Email or password is invalid !!"
        else:
            error_message = "Email password is invalid !!"
        return render(request,"login.html",{"error":error_message})

# function based logout view
def logout(request):
    request.session.clear()
    return redirect("login")


# View for homepage
class IndexView(View):

    def get(self,request):
        cart = request.session.get('cart')
        #print(request.session.items())
        if not cart:
            request.session["cart"] = {}
        category = Category.get_all_categories()
        categoryId = request.GET.get("category_url")#mention in idex.html line no 17 to sort the items according to category
        if categoryId:
            product = Product.get_all_product_by_categoryid(categoryId)
        else:
            product = Product.get_all_products()
        data = {}
        data['products']=product
        data['categorys']=category
        #print(request.session.get("email"))
        #print(request.session.get("customer_id"))
        #print(request.session)
        return render(request,'index.html',data)


    def post(self,request):
        product = request.POST.get('product')
        #print(product)
        #print(request.session)
        remove = request.POST.get("remove")
        cart = request.session.get('cart')
        #request.session["cart"]= product
        #print(cart)
        
        if cart:
            quantity = cart.get(product)
            print(quantity)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1        
                else:
                    cart[product] = quantity+1
            else:
                cart[product]=1
        else:
            cart = {}
            cart[product]=1
        request.session["cart"]= cart
        print(request.session["cart"])
        
        return redirect('homepage')
        #return HttpResponse("product added successfully")

class Cart(View):
    def get(self,request):
        #print(list(request.session.get("cart").keys()))
        ids = list(request.session.get("cart").keys())
        products = Product.get_products_by_id(ids) 
        #print(products)
        return render(request,"cart.html", {'products':products})

class CheckOut(View):
    def post(self,request):
        #print(request.POST)
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart') # quantity
        # all products
        products = Product.get_products_by_id(list(cart.keys()))

        # to get a price and create order object
        for product in products:
            #print(product)
            order = Order(customer= Customer(id=customer),
                    product= product, 
                    price= product.product_price,
                    address= address,
                    phone= phone,
                    quantity= cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}    
        return redirect('homepage')

class OrderView(View):
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request, 'orders.html', {'orders': orders})





























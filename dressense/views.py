from django.shortcuts import render,redirect
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from django.views import View
from django.contrib.auth.hashers import make_password,check_password

# Create your views here.
class Index(View):

    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect('home')
    




    def get(self,request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = None
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products();

        data = {}
        data['products'] = products
        data['categories'] = categories

        # print('you are : ', request.session.get('email'))
        return render(request, 'index.html', data)





def wishlist(request):
    return render(request,'wishlist.html')
    
def stores(request):
    return render(request,'store.html')

# def accounts(request):
#     return render(request,'account.html')

def profile(request):
    return render(request,'profile.html')



def productview(request, myid):

    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'productview.html', {'product':product[0]})



class Cart(View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request , 'cart.html' , {'products' : products} )



class Signup(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        postData = request.POST
        name = postData.get('name')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'name': name,
            'phone': phone,
            'email': email,
            'password': password
        }
        error_message = None

        customer = Customer(name=name,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = self.validateCustomer(customer)

        if not error_message:
            print(name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('home')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'register.html', data)

    def validateCustomer(self, customer):
        error_message = None;
        if (not customer.name):
            error_message = "First Name Required !!"
        elif len(customer.name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not(customer.phone):
            error_message = 'Phone Number required'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message






class Accounts(View):
    def get(self,request):
        return render(request,'account.html')



    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password,customer.password)
            if flag:
                request.session['customer'] = customer.id

                return redirect('home')
            else:
                error_message = "Email or Password is Invalid!!"
        else:
            error_message = "Email or Password is Invalid!!"
        
        return render(request,'account.html',{'error':error_message})


def logout(request):
    request.session.clear()
    return redirect('accounts')
import razorpay
from django.conf import settings
from django.shortcuts import render,reverse,redirect,get_object_or_404
from django.http import HttpResponse
from django.template import loader
from myapp.models import UserDetails
from myapp.models import Product,Cart
from .models import Cart
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from .models import Cart, Product, UserDetails, Order


# Create your views here.
def homepage(request):
    return render(request, "homepage.html")

def signuppage(request):
    return render(request, "signuppage.html")

def signupprocess(request):
    if request.method == "POST":
        uname=request.POST.get("username")
        email=request.POST.get("email")
        pwd=request.POST.get("password")
        address=request.POST.get("address")
        mobile=request.POST.get("mobile")
        altmobile=request.POST.get("altmobile")

        UserDetails.objects.create(
            username=uname,
            email=email,
            userpassword=pwd,
            address=address,
            mobilenumber=mobile,
            alternatemobile=altmobile
        )

        return redirect("login")

    return redirect("signup")
        



def loginpage(request):
    return render(request, "loginpage.html")


def adminprocess(request):
    if request.method == "POST" :
        mobile = request.POST.get("mobile")
        pwd = request.POST.get("password")

        try:
            user = UserDetails.objects.get(mobilenumber=mobile, userpassword=pwd)

            request.session['user_id'] = user.id

            products = Product.objects.all()

            return render(request, "productpage.html", {
                "user":user,
                "products": products

                
                })

        except UserDetails.DoesNotExist:
            return render(request, "loginpage.html", {"error": "Invalid mobile or password"})

    return redirect("login")

def productpage(request):
    products = Product.objects.all()
    return render(request, 'productpage.html', {'products':products})

def productdetail(request,id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'productdetail.html',{'product':product})



def add_to_cart(request, id):
    
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = UserDetails.objects.get(id=user_id)

    product = get_object_or_404(Product, id=id)

    cart_item, created = Cart.objects.get_or_create(
        user=user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')
    


def cart_page(request):
    
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = UserDetails.objects.get(id=user_id)

    items = Cart.objects.filter(user=user)

    return render(request, 'cart.html', {'items': items})



def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('productpage')
        
    else:
            form = ProductForm()

    return render(request, 'addproduct.html',{'form':form})



def place_order(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = UserDetails.objects.get(id=user_id)

    cart_items = Cart.objects.filter(user=user)

    for item in cart_items:
        Order.objects.create(
            user=user,
            product=item.product,
            quantity=item.quantity
        )


    cart_items.delete()

    return render(request, 'ordersuccess.html')




def payment_page(request):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    amount = 500 * 100  

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    return render(request, "payment.html", {
    "payment": payment,
    "key_id": settings.RAZORPAY_KEY_ID 
    
    })


def toggle_cart(request, id):
    user = UserDetails.objects.get(id=request.session['user_id'])
    product = get_object_or_404(Product, id=id)

    cart_item = Cart.objects.filter(user=user, product=product).first()

    if cart_item:
        # Product already in cart → remove it
        cart_item.delete()
    else:
        # Product not in cart → add it
        Cart.objects.create(user=user, product=product, quantity=1)

    return redirect('cart')  # redirect back to cart page





















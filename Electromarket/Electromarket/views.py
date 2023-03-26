import io
import json

from django.contrib.sites import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from app.models import slider, banner_area, Main_Category, Product, Category, Color, Brand, Coupon_Code, Wishlist, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.template.loader import render_to_string
from django.db.models import Max, Min, Sum
from cart.cart import Cart
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
import uuid
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from django.conf import settings

def BASE(request):
    return render(request, 'base.html')


def HOME(request):
    sliders = slider.objects.all().order_by('-id')[0:3]
    banners = banner_area.objects.all().order_by('-id')[0:3]
    main_category = Main_Category.objects.all()
    product = Product.objects.filter(section__name="Top Deal Of The Day")
    wishlist_items = Wishlist.objects.filter(user=request.user.id)
    context = {
        'sliders': sliders,
        'banners': banners,
        'main_category': main_category,
        'product': product,
        'wishlist_items': wishlist_items,
    }
    return render(request, 'Main/home.html', context)


def PRODUCT_DETAILS(request, slug):
    product = Product.objects.get(slug=slug)
    related_products = Product.objects.filter(Categories=product.Categories).exclude(slug= product.slug)
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'product/product_detail.html', context)


def Error404(request):
    return render(request, 'errors/404.html')


def MY_ACCOUNT(request):
    return render(request, 'account/my-account.html')


def REGISTER(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'username us already exists')
            return redirect('login')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'email id are already exists')
            return redirect('login')

        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
    return redirect('login')


def LOGIN(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email and Password are Invalid')
            return redirect('login')

@login_required(login_url='/accounts/login/')
def PROFILE(request):
    return render(request, 'profile/profile.html')

@login_required(login_url='/accounts/login/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = request.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request, 'Profile are Successfully Updated !')
        return redirect('profile')


def ABOUT(request):
    return render(request, 'Main/about.html')


def CONTACT(request):
    return render(request, 'Main/contact.html')


def PRODUCT(request):
    category = Category.objects.all()
    product = Product.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()
    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))
    ColorID = request.GET.get('colorID')
    FilterPrice = request.GET.get('FilterPrice')
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Product.objects.filter(price__lte=Int_FilterPrice)
    elif ColorID:
        product = Product.objects.filter(color=ColorID)
    else:
        product = Product.objects.all()


    context = {
        'category': category,
        'product': product,
        'min_price': min_price,
        'max_price': max_price,
        'FilterPrice': FilterPrice,
        'color': color,
        'brand': brand,
    }

    return render(request, 'product/product.html', context)


def filter_data(request):
    categories = request.GET.getlist('category[]')
    allProducts = Product.objects.all().order_by('-id').distinct()
    brand = request.GET.getlist('brand[]')

    if len(categories) > 0:
        allProducts = allProducts.filter(Categories__id__in=categories).distinct()

    if len(brand) > 0:
        allProducts = allProducts.filter(Brand__id__in=brand).distinct()

    t = render_to_string('ajax/product.html', {'product': allProducts})

    return JsonResponse({'data': t})


def SEARCH(request):
    query = request.GET.get('query')
    product = Product.objects.filter(product_name__icontains=query)

    context = {
        'product': product,
    }
    return render(request, 'includes/search.html', context)



@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def cart_detail(request):
    cart = request.session.get('cart')
    packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
    tax = sum(i['tax'] for i in cart.values() if i)

    invalid_coupon =None
    valid_coupon = None
    coupon = None
    if request.method == "GET":
        coupon_code = request.GET.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon_Code.objects.get(code=coupon_code)
                valid_coupon = "Are Applicable on Current Order!!!"
            except:
                invalid_coupon = "Invalid Coupon Code!!!"

    context = {
        'packing_cost': packing_cost,
        'tax': tax,
        'coupon': coupon,
        'valid_coupon': valid_coupon,
        'invalid_coupon': invalid_coupon,
    }
    return render(request, 'cart/cart.html', context)


def CHECKOUT(request):
    coupon_discount = None
    if request.method == "POST":
        coupon_discount = request.POST.get('coupon_discount')

    cart = request.session.get('cart')
    packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
    tax = sum(i['tax'] for i in cart.values() if i)

    tax_and_packing_cost = (packing_cost + tax)
    context = {
        'tax_and_packing_cost': tax_and_packing_cost,
        'coupon_discount': coupon_discount,
    }

    return render(request, 'checkout/checkout.html', context)


@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created:
        message = f'{product.product_name} has been added to your wishlist.'
    else:
        message = f'{product.product_name} is already in your wishlist.'

    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def remove_from_wishlist(request, wishlist_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    product_names = wishlist_item.product.product_name
    wishlist_item.delete()
    message = f'{product_names} has been removed from your wishlist.'

    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist.html', {'wishlist_items': wishlist_items})



def PLACE_ORDER(request):
    if request.method == 'POST':
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id=uid)
        cart = request.session.get('cart')
        print(cart)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        order_status = request.POST.get('order_status')
        amount = request.POST.get('amount')
        print(amount)
        payment_method = request.POST.get('payment')
        order = Order(
            user=user,
            first_name=first_name,
            last_name=last_name,
            country=country,
            address=address,
            city=city,
            state=state,
            postcode=postcode,
            phone=phone,
            email=email,
            payment_method=payment_method,
            amount=amount,
        )
        order.save()

        for i in cart:
            a = (int(cart[i]['price']))
            b = cart[i]['quantity']
            total = a * b

            item = OrderItem(
                user=user,
                order=order,
                product=cart[i]['product_name'],
                image=cart[i]['featured_image'],
                quantity=cart[i]['quantity'],
                price=cart[i]['price'],
                total=total,
            )
            item.save()
            if payment_method == "Khalti":
                return render(request, 'checkout/placeorder.html')
            if payment_method == "Cash_On_Delivery":
                return redirect('success')
    return render(request, 'checkout/placeorder.html')


def SUCCESS(request):
    return render(request, 'checkout/thank-you.html')

@csrf_exempt
def verify_payment(request):
    data =request.POST
    product_id = data['product_identity']
    token = data['token']
    amount = data['amount']
    url = "https://khalti.com/api/v2/payment/verify/"
    payload = {
        "token": token,
        "amount": amount,
    }
    headers = {
        'Authorization': 'Key test_secret_key_9cd9978f5ce64f93bfb4e77ee6c5ffdb'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response_data = json.load(response.text)
    status_code = str(response.status_code)
    if status_code == '400':
        response = JsonResponse({'status': 'false', 'message': response_data['detail']}, status=500)
        return response

    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(response_data)

    return JsonResponse(f"Payment Done !! With IDX. {response_data['user']['idx']}", safe=False)


def myOrder(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    ord = Order.objects.filter(user=request.user)
    order = OrderItem.objects.filter(order__in=ord)
    context = {
        'order': order,
        'ord': ord,
    }

    return render(request, 'checkout/myorder.html/', context)


def save_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)

    # Create a dictionary to pass to the template
    context = {
        'order': order,
        'order_items': order_items,
    }
    # Render the template with the context data
    template = get_template('download_invoice.html')
    html = template.render(context)

    # Create a PDF file from the HTML template
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF creation error', status=400)
    return response

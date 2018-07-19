from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.models import User
from django.utils import timezone
import json


# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from .models import Product, ImageModel, Cart, ProductInCart

def main_page(request):
    items = Product.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')[:5]

    return render(request, 'index.html', {'items' : items})

@login_required
def my_account(request):
    user = request.user
    return render(request, 'product-my-acount.html', {})

def about_us(request):
    user = request.user
    return render(request, 'about-us.html', {})

def contact_us(request):
    user = request.user
    return render(request, 'contact-us.html', {})


@login_required
def product_wishlist(request):
    user = request.user
    return render(request, 'product-wishlist.html', {})

@login_required
def product_cart(request):
    user = request.user
    order = get_object_or_404(Cart, user=user, status_code=0)
    carttotal = order.summary
    cart = ProductInCart.objects.filter(cart=order).order_by('-quanity')
    return render(request, 'product-cart.html', {'cart' : cart, 'carttotal': carttotal})

@login_required
def add_to_cart(request):

    if request.method == "POST":
        pk = request.POST.get('pk', None)
        count = request.POST.get('count', None)
    elif request.method == "GET":
        pk = request.GET.get('pk', None)
        count = request.GET.get('count', None)
    product = get_object_or_404(Product, article=pk)
    cart,created = Cart.objects.get_or_create(user = request.user, status_code=0)

    cartproduct = ProductInCart.objects.get_or_create(cart = cart, quanity = count, item=product)[0]
    cartproduct.summary = float(cartproduct.summary) + float(count) * float(product.price)
    cart.summary = float(cart.summary) + float(cartproduct.summary)
    cart.save()
    cartproduct.save()
    response_data = {}
    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json",
    )

@login_required
def changing_quanity(request):
    if request.method == "GET":
        pk = request.GET.get('pk', None)
        count = request.GET.get('count', None)
    logger.error(pk)
    product = get_object_or_404(Product, article=pk)
    cart = Cart.objects.get_or_create(user = request.user, status_code=0)[0]
    cartproduct = get_object_or_404(ProductInCart, cart = cart, item=product)
    cart.summary = float(cart.summary) - float(cartproduct.summary)
    cartproduct.summary = float(count) * float(product.price)
    cart.summary = float(cart.summary) + float(cartproduct.summary)
    cart.save()
    cartproduct.save()
    response_data = {}
    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json",
    )

@login_required
def delete_from_cart(request):
    art = None
    if request.method == "GET":
        art = request.GET.get('art', None)
        product = get_object_or_404(Product, article=art)
        cart = get_object_or_404 (Cart, user = request.user, status_code=0)
        cartproduct = get_object_or_404 (ProductInCart, cart = cart, item = product)
        cartproduct.delete()
        cart.summary = float(cart.summary) - float(product.price) * float(cartproduct.quanity)
        cart.save()
        response_data = {
        #Отправить сумму
        }
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json",
        )
def product_single(request, pk):
    item = get_object_or_404(Product, article=pk)
    images = ImageModel.objects.filter(item=item)
    user = request.user
    cart = get_object_or_404(Cart, user=user, status_code=0).products.filter(item = item)
    return render(request, 'product-single.html', {'item' : item, 'images' : images, 'item_already_in_cart': cart})

def product_shop(request):
    user = request.user
    items = Product.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
    return render(request, 'product-shop.html', {'items' : items})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user':user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Активируйте ваш аккаунт на BlitzShop.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Мы отправили на ваш email сообщение, необходимое для подтверждения аккаунта.')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('main_page')
    else:
        return HttpResponse('Activation link is invalid!')

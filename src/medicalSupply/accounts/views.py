from django.contrib.messages.api import error
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .form import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from cart.models import Cart, CartItem
from cart.views import _cartId

import requests


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]  

            user = Account.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                password = password,
            )
            user.phone_number = phone_number          
            user.save()

            #user activation
            # current_site = get_current_site(request) #getting current site 
            # mail_subject = 'Please activate your account'
            # message = render_to_string('accounts/account_verify.html', {
            #     'user': user,
            #     'domain':current_site,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),# encoding the user id so noone can see it
            #     'token': default_token_generator.make_token(user), # create token of the user 
            # })
            # to_email = email
            # send_email = EmailMessage(mail_subject, message, to=[to_email])
            # send_email.send()

            messages.success(request, 'Registration successful.')
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }

    return render(request, 'account/register.html', context)

#login method
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cartId(request))
                is_cart_item_exist = CartItem.objects.filter(cart=cart).exists()

                if is_cart_item_exist:
                    cart_item = CartItem.objects.filter(cart=cart)

                    for item in cart_item:
                        item.user = user
                        item.save()

            except:
                pass

            auth.login(request, user)
            messages.success(request, 'You are now logged in.')

            url =request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
                
            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login attempt.')

            return redirect('login')

    return render(request, 'account/login.html')

#logout method
@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You just log out')
    return redirect('login')




# def activate(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64.decode())
#         user = Account._default_manager.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
#         user = None

#         if user is not None and default_token_generator.check_Token(user, token):
#             user.is_active = True
#             user.save()
#             messages.success(request, 'Your account is activated')
#             return redirect('login')
#         else:
#             messages.error(request, 'Invalid activation link.')
#             return redirect('register')

# method to render dashboard page
@login_required(login_url='login')
def dashboard(request):

    return render(request, 'account/dashboard.html')


def forgotPassword(request):
    if request.method == "POST":
        email = request.POST['email']

        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            
            #passwrod reset via email
            current_site = get_current_site(request) #getting current site 
            mail_subject = 'Reset your password'
            message = render_to_string('account/reset_password.html', {
                'user': user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),# encoding the user id so noone can see it
                'token': default_token_generator.make_token(user), # create token of the user 
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, "Password reset email has been sent to your email address.")

            return redirect('login')
             
        
        else:
            messages.error(request, 'Account doesnt not exists.')
            return redirect('forgotPassword')

    return render(request, 'account/forgotPassword.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired.')
        return redirect('login')

def resetPassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')# getting uid from the sessing saved when validating
            user = Account.objects.get(pk=uid)
            user.set_password(password) # take the password and save it in hash format
            user.save()
            messages.success(request, 'Password reset successful.')
            return redirect('login')
            
        else:
            messages.error(request, 'Password do not match')
            return redirect('resetPassword')

    return render(request, 'account/resetPassword.html')
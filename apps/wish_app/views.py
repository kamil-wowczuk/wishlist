# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.messages import get_messages
from django.contrib import messages
from django.db.models import Count
from .models import User, Product

# Create your views here.

def index(request):

    context = {
        'messages':get_messages(request)
    }

    return render(request, "main/index.html", context)

def login(request):
    print ' Got to login '
    if request.method == "POST":
        print ' Got past post '
        post_data = {
            'email':request.POST['email'],
            'password':request.POST['password']
        }
        print 'Sending data to models for authentication ... '
        login_result = User.objects.login(post_data)
        print login_result


        if login_result['result'] == "failed_authentication":
            print "login result returned failed authentication"
            if 'messages' in login_result.keys():
                for message in login_result['messages']:
                    messages.error(request, message)
            return redirect('/')
        else:
            if 'user' in login_result.keys():
                request.session['current_user'] = login_result['user'].id
                # if 'messages' in login_result.keys():
                #     for message in login_result['messages']:
                #         messages.success(request, message)
            else:
                messages.error(request, "Something went wrong")
                return redirect('/')

            return redirect('/dashboard')


def register(request):
    if request.method == "POST":

        post_data = {
            'name':request.POST['name'],
            'date_hired':request.POST['date'],
            'email':request.POST['email'],
            'password':request.POST['password'],
            'confirm_password':request.POST['confirm_password'],
            'date_hired':request.POST['date'],
        }
        print ' Date hired ', post_data['date_hired']
        register_result = User.objects.register(post_data)
        print register_result

        if register_result['result'] == "failed_validation":
            if 'messages' in register_result.keys():
                for message in register_result['messages']:
                    messages.error(request, message)
            return redirect('/')
        else:
            if 'user' in register_result.keys():
                request.session['current_user'] = register_result['user'].id
                if 'messages' in register_result.keys():
                    for message in register_result['messages']:
                        messages.success(request, message)
            else:
                messages.error(request, "Something went wrong")
                return redirect('/')
            return redirect('/dashboard')

    return redirect('/')

def dashboard(request):
    user_id = request.session['current_user'] 
    user = User.objects.get(pk=user_id)
    products = Product.objects.exclude(created_by__pk=user_id)
    context = {
        'my_products':user.products.all(),
        'user':user,
        'products':products,
    }
    print 'This is user ', user




    return render(request, 'main/dashboard.html', context)

def wish_items(request, product_id):
    product = Product.objects.get(pk=product_id)
    context = {
        'product':product
    }
    return render(request, 'main/wish_items.html', context)

def create(request):
    user = User.objects.get(pk=request.session['current_user'])
    print user
    if request.method == 'POST':
        if len(request.POST['name']) > 3:
            product = Product.objects.create(name=request.POST['name'], created_by=user)
            user.products.add(product)
            return redirect('/dashboard')
        elif len(request.POST['name']) == 0:
            messages.error(request, 'Product name cannot be empty')
            return render(request, 'main/create.html')
        else:
            messages.error(request, 'Product name has to be longer than')
            return render(request, 'main/create.html')
    return render(request, 'main/create.html')


def add_product(request):
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def add(request, product_id):
    user = User.objects.get(pk=request.session['current_user'])
    product = Product.objects.get(pk=product_id)
    user.products.add(product)
    return redirect('/dashboard')

def remove(request, product_id):
    user = User.objects.get(pk=request.session['current_user'])
    product = user.products.get(pk=product_id)
    user.products.remove(product)
    return redirect('/dashboard')

def delete(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.delete()
    return redirect('/dashboard')
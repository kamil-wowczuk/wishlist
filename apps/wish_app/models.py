# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models
import bcrypt, re, datetime
from datetime import datetime


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z ]+$')


class UserManager(models.Manager):
    def login(self, postData):
        print 'Starting login authentication ... '
        failed_authentication = False
        messages = []

        try:
            found_user = User.objects.get(email=postData['email'])
        except:
            found_user = False

        if len(postData['email']) < 1:
            messages.append("Email cannot be left blank!")
            failed_authentication = True
        elif not EMAIL_REGEX.match(postData['email']):
            messages.append("Please enter a valid email!")
            failed_authentication = True
        elif not found_user:
            messages.append("No user found with this email address. Please register new user.")
            failed_authentication = True

        if failed_authentication:
            return {'result':"failed_authentication", 'messages':messages}

        if len(postData['password']) < 8:
            messages.append("Password must be at least 8 characters")
            return {'result':"failed_authentication", 'messages':messages}


        hashed_password = bcrypt.hashpw(str(postData['password']), str(found_user.salt))

        if found_user.password != hashed_password:
            messages.append("Incorrect password! Please try again")
            failed_authentication = True


        if failed_authentication:
            return {'result':"failed_authentication", 'messages':messages}
        else:
            messages.append('Successfully logged in!')
            return {'result':'success', 'messages':messages, 'user':found_user}

    def register(self, postData):

        failed_validation = False
        messages = []

        if len(postData['name']) < 2:
            messages.append("Name must be at least 2 characters!")
            failed_validation = True
        elif not NAME_REGEX.match(postData['name']):
            messages.append("Name can only contain letters or spaces!")
            failed_validation = True

        try:
            found_user = User.objects.get(email=postData['email'])
        except:
            found_user = False

        if len(postData['email']) < 1:
            messages.append("Email is required!")
            failed_validation = True
        elif not EMAIL_REGEX.match(postData['email']):
            messages.append("Please enter a valid email!")
            failed_validation = True
        elif found_user:
            messages.append("This email is already registered!")
            failed_validation = True

        if len(postData['password']) < 1:
            messages.append("Password is required!")
            failed_validation = True
        elif len(postData['password']) < 8:
            messages.append("Password must be at least 8 characters")
            failed_validation = True
        elif postData['confirm_password'] != postData['password']:
            messages.append("Password confirmation failed")
            failed_validation = True

        if failed_validation:
            return {'result':"failed_validation", 'messages':messages}

        salt = bcrypt.gensalt()

        hashed_password = bcrypt.hashpw(str(postData['password']), str(salt))

        User.objects.create(name=postData['name'], email=postData['email'], password=hashed_password, salt=salt, date_hired=postData['date_hired'])


        user = User.objects.get(email=postData['email'])

        return {'result':"Successfully registered new user", 'messages':messages, 'user':user}



class User(models.Model):
    name = models.CharField(max_length=45)
    email = models.EmailField()
    password = models.CharField(max_length=45)
    date_hired = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    salt = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    objects = UserManager()

class Product(models.Model):
    name = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)
    users = models.ManyToManyField(User, related_name='products')
    def __str__(self):
        return self.name


# Create your models here.

from django.shortcuts import render, redirect,HttpRespone
from .mongo import users_collection
from .forms import UserForm
from pymongo import MongoClient

def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Insert new user into MongoDB
            user_data = form.cleaned_data
            users_collection.insert_one(user_data)
            return HttpRespone("Added Successfully")
    else:
        form = UserForm()
    return render(request, 'user_form.html',{"form":form})


from django.shortcuts import render, redirect
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
            return redirect('create-user')
    else:
        form = UserForm()
    context ={"form":form}
    return render(request, 'user_form.html',context)

def index(request):
    return render(request, "user_form.html")



   
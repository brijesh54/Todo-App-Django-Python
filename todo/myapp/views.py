from django.urls import reverse_lazy
from .models import CrudUser
from django.views.generic import TemplateView, View, DeleteView
from django.views.generic import ListView
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate , login as loginUser , logout
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method == 'GET':
        form1 = AuthenticationForm()
        context = {
            "form" : form1
        }
        return render(request , 'login.html' , context=context )
    else:
        form = AuthenticationForm(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username , password = password)
            if user is not None:
                loginUser(request , user)
                return redirect('crud_ajax')
        else:
            context = {
                "form" : form
            }
            return render(request , 'login.html' , context=context )


def signup(request):

    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            "form" : form
        }
        return render(request , 'signup.html' , context=context)
    else:
        # print(request.POST)
        form = UserCreationForm(request.POST)  
        context = {
            "form" : form
        }
        if form.is_valid():
            messages.success(request,'acoount created successfully')
            user = form.save()
            # print(user)
            if user is not None:
                return redirect('login')
        else:
            return render(request , 'signup.html' , context=context)

def signout(request):
    logout(request)
    return redirect('login')

class CrudView(ListView):
    model = CrudUser
    template_name = 'crud.html' 
    context_object_name = 'users'

class CreateCrudUser(View):
    def  get(self, request):
        title1 = request.GET.get('title', None)
        status1 = request.GET.get('status', None)
        priority1 = request.GET.get('priority', None)

        obj = CrudUser.objects.create(
            title = title1,
            status = status1,
            priority = priority1
        )

        user = {'id':obj.id,'title':obj.title,'status':obj.status,'priority':obj.priority}

        data = {
            'user': user
        }
        return JsonResponse(data)

class DeleteCrudUser(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        CrudUser.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


class UpdateCrudUser(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        title1 = request.GET.get('title', None)
        status1 = request.GET.get('status', None)
        priority1 = request.GET.get('priority', None)

        obj = CrudUser.objects.get(id=id1)
        obj.title = title1
        obj.status = status1
        obj.priority = priority1
        obj.save()

        user = {'id':obj.id,'title':obj.title,'status':obj.status,'priority':obj.priority}

        data = {
            'user': user
        }
        return JsonResponse(data)
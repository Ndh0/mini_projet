from asyncio.base_futures import _PENDING
from django.http import HttpRequest, HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.db.models.signals import post_save
from django.dispatch import receiver

from PIL import Image as Im
import ArtyProd
from .forms import *
from .models import * 
from django.core.files import File
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

def register(request):
    if request.method == 'POST' :
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            return redirect('EditPersonnel', id=user.personnel.id)
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


        

def FileUploader(request):
    file_variable = request.FILES['file']  # assume this is your file variable
    file_object = File(file_variable)
    return render(request, 'my_template.html', {'file_object': file_object})


def index(request):  
    #if request.user.is_superuser:
     #   return redirect('/admin')
    #else:
    list=Projet.objects.filter(status=True)
    return render( request,'home.html',{'list':list})

def signinpage(request):
    return render(request,'ArtyProd/signin.html')
# Create your views here.
@login_required
def ServiceList(request):   
    list=Service.objects.all()
    return render( request,'ArtyProd/servicelist.html',{'list':list})

def ProjetList(request):   
    list=Projet.objects.filter(status=True)
    return render( request,'ArtyProd/projetlist.html',{'list':list})

def ProjetFilter(request):   
    #list=Projet.objects.all()
    user_name = request.user
    list = Projet.objects.filter(equipe__personnels__nom__icontains=user_name.first_name)

    return render( request,'ArtyProd/projetlist.html',{'list':list})
#def books_by_author(request, author_id):
    author = Author.objects.get(id=author_id)
    books = Book.objects.filter(author=author)
    return render(request, 'books_by_author.html', {'books': books})

@login_required
def EquipeList(request):  
    list=Equipe.objects.all()
    return render( request,'ArtyProd/equipelist.html',{'list':list})

@login_required
def PersonnelList(request):   
    list=Personnel.objects.all()
    return render( request,'ArtyProd/personnellist.html',{'list':list})

def ServiceAdd(request):
    if request.method=="POST":
        form=ServiceForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ArtyProd/servicelist')#*-->
    else:
        form=ServiceForm()
    return render(request,'ArtyProd/serviceadd.html',{'form':form})

def admin_panel(request):
    projects_to_approve = Projet.objects.filter(status=False)
    return render(request, 'admin/admin_panel.html', {'projects_to_approve': projects_to_approve})


def approve_project(request, project_id):
    project = get_object_or_404(Projet, pk=project_id)
    project.status = True
    project.save()
    return redirect('admin_panel')

def ProjetAdd(request):
    if request.method=="POST":
        form=ProjetForm(request.POST,request.FILES)
        if form.is_valid():
            projet = form.save(commit=False)
            projet.approved = False
            form.save()
            
            return HttpResponseRedirect('/ArtyProd/projetlist')#*-->
    else:
        form=ProjetForm()
    return render(request,'ArtyProd/projetadd.html',{'form':form})


def PersonnelAdd(request):
    if request.method=="POST":
        form=PersonnelForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ArtyProd/personnellist')#*-->
    else:
        form=PersonnelForm()
    return render(request,'ArtyProd/personneladd.html',{'form':form})


def EquipeAdd(request):
    if request.method=="POST":
        form=EquipeForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ArtyProd/equipelist')#*-->
    else:
        form=EquipeForm()
    return render(request,'ArtyProd/equipeadd.html',{'form':form})

def EditService(request, id):
    post = get_object_or_404(Service, id=id)

    if request.method == 'GET':
        context = {'form': ServiceForm(instance=post), 'id': id}
        return render(request,'ArtyProd/editservice.html',context)
    elif request.method == 'POST':
        form = ServiceForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ArtyProd/servicelist')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request,'ArtyProd/editservice.html',{'form':form})    

def EditEquipe(request, id):
    post = get_object_or_404(Equipe, id=id)

    if request.method == 'GET':
        context = {'form': EquipeForm(instance=post), 'id': id}
        return render(request,'ArtyProd/editequipe.html',context)
    elif request.method == 'POST':
        form = EquipeForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ArtyProd/equipelist')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request,'ArtyProd/editequipe.html',{'form':form})    
@login_required
def EditPersonnel(request, id):
    personnel = get_object_or_404(Personnel, id=id, user=request.user)

    if request.method == 'GET':
        context = {'form': PersonnelForm(instance=personnel), 'id': id}
        return render(request, 'ArtyProd/editpersonnel.html', context)
    elif request.method == 'POST':
        form = PersonnelForm(request.POST, request.FILES, instance=personnel)
        if form.is_valid():
            form.save()
            messages.success(request, 'Personnel updated successfully.')
            return HttpResponseRedirect('/ArtyProd/personnellist')
        else:
            messages.error(request, 'Please correct the following errors:')
        context = {'form': form, 'id': id}
        return render(request, 'ArtyProd/editpersonnel.html', context)


  
  

def EditProjet(request, id):
    post = get_object_or_404(Projet, id=id)

    if request.method == 'GET':
        context = {'form': ProjetForm(instance=post), 'id': id}
        return render(request,'ArtyProd/editprojet.html',context)
    elif request.method == 'POST':
        form = ProjetForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ArtyProd/projetlist')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request,'ArtyProd/editprojet.html',{'form':form})

def deleteService(request,pk):   
        Service.objects.filter(id=pk).delete()
        return HttpResponseRedirect('/ArtyProd/servicelist')

def deleteProjet(request,pk):   
        Projet.objects.filter(id=pk).delete()
        return HttpResponseRedirect('/ArtyProd/projetlist')

def deletePersonnel(request,pk):   
        Personnel.objects.filter(id=pk).delete()
        return HttpResponseRedirect('/ArtyProd/personnellist')

def deleteEquipe(request,pk):   
        Equipe.objects.filter(id=pk).delete()
        return HttpResponseRedirect('/ArtyProd/equipelist')




def increment_avisp(request, id):
    # Get the project object by ID
    project = get_object_or_404(Projet, id=id)

    # Increment the value of avisp by 1
    project.avisp += 1
    project.save()
    return HttpResponseRedirect('/ArtyProd/projetlist')

def decrement_avisn(request, id):
    # Get the project object by ID
    project = get_object_or_404(Projet, id=id)

    # Increment the value of avisp by 1
    project.avisn += 1
    project.save()
    return HttpResponseRedirect('/ArtyProd/projetlist')




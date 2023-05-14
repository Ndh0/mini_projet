from tkinter.ttk import Style
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.admin import UserAdmin

class ServiceForm(ModelForm): 
    class Meta : 
        model = Service
        fields = "__all__"
        widgets = {
            'description' : forms.TextInput(attrs={'class': 'form-control'}),
            'type' : forms.Select(attrs={'class': 'form-control'}),
            'Details' : forms.Select(attrs={'class': 'form-select form-select-lg mb-3'}),
        }

class ProjetForm(ModelForm): 
    class Meta : 
        model = Projet 
        fields = "__all__"
        exclude = ('status','acheve','avisp','avisn')
        widgets = {
           'libelle' : forms.TextInput(attrs={'class': 'form-control'}),
            'description' : forms.TextInput(attrs={'class': 'form-control'}),
            'services' : forms.Select(attrs={'class': 'form-control'}),
            'equipe' : forms.Select(attrs={'class': 'form-control'}),
        }

class PersonnelForm(ModelForm): 
    class Meta : 
        model = Personnel 
        fields = "__all__"
        exclude = ('user','acheve')
        widgets = {
            'nom' : forms.TextInput(attrs={'class': 'form-control'}),
            'fichier_CV' : forms.FileInput(attrs={'required': False,'class': 'form-control','enctype': 'multipart/form-data'}),
            'fichier_photo' : forms.FileInput(attrs={'required': False,'class': 'form-control','enctype': 'multipart/form-data'}),
            'lien_linkedln' : forms.TextInput(attrs={'class': 'form-control'}),
        }

class EquipeForm(ModelForm): 
    class Meta : 
        model = Equipe 
        fields = "__all__"
        widgets = {
            'personnels' : forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class UserRegistrationForm(UserCreationForm):
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    telephone = forms.DecimalField(label='tel',max_digits=8,widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username','first_name', 'last_name' , 'email','telephone','password1','password2','user_type')
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['class']='form-control'




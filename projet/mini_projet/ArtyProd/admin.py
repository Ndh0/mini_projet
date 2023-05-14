from django.contrib import admin
from .models import *
admin.site.register(Service)
admin.site.register(Personnel)
admin.site.register(Detail)
admin.site.register(Equipe)
admin.site.register(Projet)
admin.site.register(Client)
from django.shortcuts import render,redirect
from django import forms
from .models import Projet
from .decorators import action_form
from .models import CustomUser

admin.site.register(CustomUser)

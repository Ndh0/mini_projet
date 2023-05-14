from django.urls import path   
from . import views

urlpatterns = [	
    path('', views.index,name='home'),
    path('signin/',views.signinpage),
    path('serviceadd/',views.ServiceAdd),
    path('projetadd/',views.ProjetAdd),
    path('personneladd/',views.PersonnelAdd),
    path('equipeadd/',views.EquipeAdd),
    path('equipelist/',views.EquipeList),
    path('servicelist/',views.ServiceList),
    path('projetlist/',views.ProjetList),
    path('myproject/',views.ProjetFilter,name='projetfilter'),
    path('adminpanel/',views.admin_panel,name='admin_panel'),
    path('approve-project/<int:project_id>/', views.approve_project, name='approve_project'),
    path('personnellist/',views.PersonnelList),
    path('editservice/edit/<int:id>/', views.EditService, name='service-edit'),
    path('editequipe/edit/<int:id>/', views.EditEquipe, name='equipe-edit'),
    path('editprojet/edit/<int:id>/', views.EditProjet, name='projet-edit'),
    path('editpersonnel/edit/<int:id>/', views.EditPersonnel, name='EditPersonnel'),
    path('deletepersonnel/delete/<int:pk>/', views.deletePersonnel, name='delete-personnel'),
    path('deleteservice/delete/<int:pk>/', views.deleteService, name='delete-service'),
    path('deleteprojet/delete/<int:pk>/', views.deleteProjet, name='delete-projet'),
    path('deleteequipe/delete/<int:pk>/', views.deleteEquipe, name='delete-equipe'),
    path('register/',views.register, name = 'register'),
    path('projetavisp/<int:id>/', views.increment_avisp, name='increment_avisp'),
    path('projetavisn/<int:id>/', views.decrement_avisn, name='decrement_avisn'),

    ]

from email.policy import default
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('personnel', 'Personnel'),
        ('client', 'Client'),
    ]
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='client',
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    def save(self, *args, **kwargs):
        if not self.pk:
            return super().save(*args, **kwargs)

#class Detail
class Detail(models.Model):
    fichier=models.FileField(upload_to='uploads/',max_length=255)#mediRoot

#Class service 
class Service(models.Model):
    types=[
        ('dg','Design Graphique'),
        ('pa','Production Audiovisuelle'),
        ('c3d','Conception 3D')
    ]   
    description=models.CharField(max_length=255)
    type=models.CharField(max_length=255,choices=types,default='dg')
    details=models.ForeignKey(Detail,on_delete=models.CASCADE)
    def __str__(self):
        return "\nType : "+self.type+"\n"



#class Personnel
class Personnel(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,default=None)
    nom=models.CharField(max_length=255)
    fichier_CV=models.FileField(upload_to='uploads/',max_length=255,default=None)
    fichier_photo=models.ImageField(upload_to='media/',max_length=255,default=None)
    lien_linkedln=models.CharField(max_length=255,default="")
    def __str__(self):
        return "\nNom : "+self.nom+" Lien Linkedln : "+self.lien_linkedln

@receiver(post_save, sender=CustomUser)
def create_personnel_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == "personnel":
        Personnel.objects.create(user=instance)

class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,default=None)
    nom=models.CharField(max_length=255)
    email=models.EmailField(max_length=255,default="")
    telephone=models.DecimalField(max_digits=8,decimal_places=2)
    def __str__(self):
        return "\nNom : "+self.nom+" email : "+self.email

@receiver(post_save, sender=CustomUser)
def create_client_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == "client":
        Client.objects.create(user=instance)

#Class Equipe
class Equipe(models.Model):
    #tableau des personnels !
    personnels=models.ManyToManyField(Personnel)

    def __str__(self):
        personnel_list = ", ".join(personnel.nom for personnel in self.personnels.all())
        i=self.id
        return f"Equipe {i} : ({personnel_list})"


#class Projet
class Projet(models.Model):
    status = models.BooleanField(default=False)
    libelle=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    date_debut=models.DateField()
    date_fin=models.DateField()
    acheve=models.BooleanField(default=False)
    services=models.ForeignKey(Service,on_delete=models.CASCADE)
    equipe=models.OneToOneField(Equipe,on_delete=models.CASCADE,default=None)
    avisp=models.DecimalField(default=0,decimal_places=0,max_digits=999)
    avisn=models.DecimalField(default=0,decimal_places=0,max_digits=999)
    def __str__(self):
        return "\nLibelle : "+self.libelle+" DateFin : "+str(self.date_fin)+" Achevee : "+str(self.acheve)




# Create your models here.

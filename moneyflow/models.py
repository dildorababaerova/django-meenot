from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db import models


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: 
        abstact =True

class OwnedModel(models.Model):
    owner = models.ForeignKey(
    settings.AUTH_USER_MODEL, 
    on_delete=models.CASCADE,)




class Document(TimestampModel, OwnedModel):
    class Type(models.TextChoices):
        BILL = ("BILL", _("LASKU"))
        RECEIPT = ("RECEIPT", _("Kuitti"))
        CALCULATION = ("CALCULATION", _("Laskelma"))
        OTHER = ("OTHER", _("Muu"))

    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=Type.choices)
    file = models.FileField(upload_to="docs/%Y-%m/")
    


class Category(TimestampModel,OwnedModel):
    name =models.CharField(max_length=100)
    parent = models.ForeignKey(
    "self",
    blank=True,
    null=True,
    related_name="children",
    on_delete=models.CASCADE,
    )
    


class Account(TimestampModel,OwnedModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,)
    name =models.CharField(max_length=200)
    bank_account =models.CharField(max_length=50, null =True, blank=True)

class Transaction(TimestampModel):
    class Type(models.TextChoices):
        INCOME = ("INCOME", _("Tulo"))
        EXPENSE = ("EXPENSE", _("Meno"))

    class State(models.TextChoices):
        UPCOMING = ("UPCOMING", _("Tuleva"))
        DONE = ("DONE", _("Tapahtunut"))

    
    state = models.CharField(max_length=20, choices=State.choices)
    date = models.DateField()
    category= models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    account = models.ForeignKey(Account, on_delete=models.RESTRICT)
    documents = models.ManyToManyField(Document, related_name="transactions", blank=True,)



    type = models.CharField(max_length=20, choices=Type.choices)
    
    
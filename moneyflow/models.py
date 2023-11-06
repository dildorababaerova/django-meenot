from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db import models


class TimestampModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("luotu"),
        )
    
    class Meta: 
        abstract =True

class OwnedModel(models.Model):
    owner = models.ForeignKey(
    settings.AUTH_USER_MODEL, 
    on_delete=models.CASCADE,
    verbose_name=_("omistaja"))
    
    class Meta: 
        abstract =True




class Document(TimestampModel, OwnedModel):
    class Type(models.TextChoices):
        #KOODi_NIMI = ("Tietokantaan TLENNTTAVA", _("Käyttäjälle näkyvä"))
        BILL = ("BILL", _("Lasku"))
        RECEIPT = ("RECEIPT", _("Kuitti"))
        CALCULATION = ("CALCULATION", _("Laskelma"))
        OTHER = ("OTHER", _("Muu"))

    type = models.CharField(
        max_length=20,
        choices=Type.choices,
        verbose_name=_("tyyppi"),
        )
    name = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name=_("nimi"),
        )
    file = models.FileField(
        upload_to="docs/%Y-%m/",
        verbose_name=_("tiedosto"),
        )
    
    class Meta:
        verbose_name=_("dokumentti")
        verbose_name_plural=_("dokumentit")

    def __str__(self):
        return self.name if self.name else f"Document {self.id}"
    


class Category(TimestampModel,OwnedModel):
    name =models.CharField(
        max_length=100,
        verbose_name=_("nimi"),
        )
    parent = models.ForeignKey(
    "self",
    blank=True,
    null=True,
    related_name="subcategories",
    on_delete=models.CASCADE,
    verbose_name=_("yläkategoria"),
    )

    class Meta:
        verbose_name=_("kategoria")
        verbose_name_plural=_("kategoriat")
    
    def __str__(self):
        prefix = f"{self.parent} / " if self.parent else ""
        return f"{prefix}{self.name}"

class Account(TimestampModel,OwnedModel):
    name =models.CharField(
        max_length=100,
        )
    bank_account =models.CharField(max_length=50, null =True, blank=True)

    def __str__(self):
        return f"{self.id:04d} {self.name}"
    

class Transaction(TimestampModel):
    class Type(models.TextChoices):
        INCOME = ("INCOME", _("Tulo"))
        EXPENSE = ("EXPENSE", _("Meno"))

    class State(models.TextChoices):
        UPCOMING = ("UPCOMING", _("Tuleva"))
        DONE = ("DONE", _("Tapahtunut"))

    account = models.ForeignKey(Account, on_delete=models.RESTRICT)
    type = models.CharField(max_length=20, choices=Type.choices)
    state = models.CharField(max_length=20, choices=State.choices)
    date = models.DateField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    category= models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    documents = models.ManyToManyField(Document, related_name="transactions", blank=True,)

    documents = models.ManyToManyField(
        Document, 
        related_name="transactions",
        blank=True,
    )

    def __str__(self):
        return f"{self.date} {self.account} {self.amount} ({self.state})"

    
    
    
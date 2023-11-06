from django.shortcuts import render
from .models import Account

def frontpage(request):
    
    context ={
        "accounts":Account.objects.all(),
    }

    return render(request, "moneyflow/index.html")

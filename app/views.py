from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from app.forms import TicketForm


@login_required
def home_page(request):
    return render(request, "app/home_page.html")


@login_required
def create_ticket(request):
    form = TicketForm()
    return render(request, "app/create_ticket.html", {"form": form})

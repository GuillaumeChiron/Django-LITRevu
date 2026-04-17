from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from app.models import Ticket, Review
from app.forms import TicketForm


@login_required
def home_page(request):
    tickets = Ticket.objects.all()
    return render(request, "app/home_page.html", {"tickets": tickets})


@login_required
def create_ticket(request):
    form = TicketForm()
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("home-page")
    return render(request, "app/create_ticket.html", {"form": form})

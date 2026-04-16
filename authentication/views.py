from django.shortcuts import render, redirect

from authentication import forms
from django.contrib.auth.forms import UserCreationForm


def signup_page(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        form.save()
        return redirect("login-page")
    return render(request, "authentication/signup_page.html", {"form": form})

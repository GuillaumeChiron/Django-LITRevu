from django.shortcuts import render, redirect

from authentication import forms
from authentication.forms import SignupForm


def signup_page(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("login-page")
    return render(request, "authentication/signup_page.html", {"form": form})

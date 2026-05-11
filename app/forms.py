from django import forms
from app.models import Review, Ticket


# Formulaire des tickets
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ["user"]


# Formulaire des reviews
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ["user", "ticket"]

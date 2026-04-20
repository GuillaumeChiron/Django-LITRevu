from django import forms
from app.models import Review, Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ["user"]


class ReviewResponseForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ["user", "ticket"]

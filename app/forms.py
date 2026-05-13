from django import forms
from app.models import Review, Ticket


# Formulaire des tickets
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


# Formulaire des reviews
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "headline", "body"]

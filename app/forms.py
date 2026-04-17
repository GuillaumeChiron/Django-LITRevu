from django import forms
from app.models import Review, Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = "__all__"

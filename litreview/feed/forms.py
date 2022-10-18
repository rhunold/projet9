from django import forms

from feed.models import Ticket


class TicketForm(forms.ModelForm):
   class Meta:
     model = Ticket
     fields = '__all__'
    #  exclude = ('time_created',)  # pour ne pas afficher certains champs du model dans le formulaire
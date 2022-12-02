from django import forms
from feed.models import Ticket, Review


# Value, Label
RATINGS = [('0', 0), ('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)]


class TicketForm(forms.ModelForm):
    """ Ticket form """

    class Meta:
        model = Ticket

        # fields = '__all__'
        # exclude = ('user',)  # pour ne pas afficher certains champs du model dans le formulaire
        fields = ['title', 'description', 'image', ]

        labels = {
          "title": "Titre",
          "description": "Description",
          "image": "Image",
          }


class ReviewForm(forms.ModelForm):
    """ Review form """

    rating = forms.ChoiceField(label='Note', widget=forms.RadioSelect, choices=RATINGS)

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body', ]
        labels = {
          "headline": "Titre",
          "rating": "Note",
          "body": "Commentaire",
          }
        # widgets = {
        #   'ticket': forms.HiddenInput,
        #   }


class TicketReviewForm(forms.Form):
    """ Ticket and Review form """
    title = forms.CharField(label='Titre', max_length=128)
    description = forms.CharField(label='Description', max_length=2048, required=False,
                                  widget=forms.Textarea(attrs={'rows': '10', 'cols': '50'}))
    image = forms.ImageField(label='Image', required=False)
    headline = forms.CharField(label='Titre', max_length=128)
    rating = forms.ChoiceField(label='Note', widget=forms.RadioSelect, choices=RATINGS)
    body = forms.CharField(label='Commentaire', max_length=8192, required=False,
                           widget=forms.Textarea(attrs={'rows': '10', 'cols': '50'}))


class DeleteTicketForm(forms.Form):
    """ Delete a Ticket """
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class DeleteReviewForm(forms.Form):
    """ Delete a Review """
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

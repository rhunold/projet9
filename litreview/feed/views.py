from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

from feed.models import Ticket, Review

from feed.forms import TicketForm

def login(request):
    return HttpResponse('<h1>Hello Django!</h1>')

def ticket_list(request):
    tickets = Ticket.objects.all()
    # reviews = Review.objects.all()    
    return render(request, 'feed/ticket_list.html', {'tickets': tickets})


def ticket_detail(request, id):
    ticket = Ticket.objects.get(id=id)
    return render(request, 'feed/ticket_detail.html', {'ticket': ticket})


def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            # créer une nouvelle « Band » et la sauvegarder dans la db
            ticket = form.save()
            # redirige vers la page de détail du groupe que nous venons de créer
            # nous pouvons fournir les arguments du motif url comme arguments à la fonction de redirection
            return redirect('ticket_detail', ticket.id)

    else:
        form = TicketForm()

    return render(request, 'feed/ticket_create.html', {'form': form})


def ticket_update(request, id):
    ticket = Ticket.objects.get(id=id)
    
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            # mettre à jour le groupe existant dans la base de données
            form.save()
            # rediriger vers la page détaillée du groupe que nous venons de mettre à jour
            return redirect('ticket_detail', ticket.id)
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'feed/ticket_update.html', {'form': form})
    
def ticket_delete(request, id):
    ticket = Ticket.objects.get(id=id)
# listings/views.py

def ticket_delete(request, id):
    ticket = Ticket.objects.get(id=id)

    if request.method == 'POST':
        # supprimer le groupe de la base de données
        ticket.delete()
        # rediriger vers la liste des groupes
        return redirect('ticket_list')

    # pas besoin de « else » ici. Si c'est une demande GET, continuez simplement

    return render(request, 'feed/ticket_delete.html', {'ticket': ticket})

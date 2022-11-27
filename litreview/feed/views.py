# from django.http import HttpResponse
from django.shortcuts import render, redirect

from feed.models import Ticket, Review
from authentication.models import UserFollow
from feed.forms import TicketForm, ReviewForm, TicketReviewForm  # DeleteReviewForm, DeleteTicketForm

from django.contrib.auth.decorators import login_required


from itertools import chain



@login_required
def home(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    
    followings = UserFollow.objects.filter(user=request.user)
    for following in followings:
        tickets = tickets | Ticket.objects.filter(user=following.followed_user)
        reviews = reviews | Review.objects.filter(user=following.followed_user)
        
    tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda x: x.time_created, reverse=True) 
    
    reviews_ticket = [review.ticket for review in reviews]
    
    context = {
        'tickets_and_reviews': tickets_and_reviews,
        'reviews_ticket': reviews_ticket,        
        }

    if request.method == 'POST':
      
        ticket_id = Ticket.objects.filter(id=request.POST["ticket_id"])

        return render(request, 'feed/review_create.html', ticket_id=ticket_id)        
    
    return render(request, 'feed/home.html', context=context)


# POSTS 
@login_required
def posts(request):
    tickets = Ticket.objects.filter(user=request.user) 
    reviews = Review.objects.filter(user=request.user)
    
    tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda x: x.time_created, reverse=True) 
    
    context = {
        'tickets': tickets,
        'reviews': reviews,   
        'tickets_and_reviews': tickets_and_reviews,
        }            
    return render(request, 'feed/posts.html', context=context)



@login_required
def ticket_review_create(request):
    """ Create ticket & review """
    
    if request.method == 'POST':
        form = TicketReviewForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = Ticket(
                title = form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                image = form.cleaned_data.get('image'),
                user = request.user
            )
            ticket.save()

            review = Review(
                headline = form.cleaned_data['headline'],
                rating = form.cleaned_data['rating'],
                body = form.cleaned_data['body'],
                ticket = ticket,
                user = request.user
            )
            review.save()
            
            return redirect('/home/')            


    else:
        form = TicketReviewForm()
        
    context = {
        # 'ticket_form': ticket_form,
        # 'review_form': review_form,   
        'form': form,           
        }              

    return render(request, 'feed/ticket_review_create.html', context=context)

@login_required
def ticket_detail(request, ticket_id):
    """ Ticket detail view """    
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, 'feed/ticket_detail.html', {'ticket': ticket})


@login_required
def ticket_create(request):
    """ Create Ticket """   
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')            

    else:
        form = TicketForm()

    return render(request, 'feed/ticket_create.html', {'form': form})


# Mettre un decorateur de permission
@login_required
def ticket_update(request, ticket_id):
    """ Update Ticket """       
    ticket = Ticket.objects.get(id=ticket_id)
    update_form = TicketForm(instance=ticket)
    
    if request.method == 'POST':
        update_form = TicketForm(request.POST, instance=ticket)
        if update_form.is_valid():
            update_form.save()
            return redirect('home')

    context = {
        'update_form': update_form,
        'ticket': ticket,
        }
    
    return render(request, 'feed/ticket_update.html', context=context)


@login_required
def ticket_delete(request, ticket_id):
    """ Delete Ticket"""       
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('home')
    return render(request, 'feed/ticket_delete.html', {'ticket': ticket})


# REVIEW


@login_required
def review_create(request, ticket_id):
    """ Create a review for a ticket """       

    ticket = Ticket.objects.get(id=ticket_id)
     
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():        
            review = Review(
                headline = form.cleaned_data['headline'],
                rating = form.cleaned_data['rating'],
                body = form.cleaned_data['body'],
                ticket = ticket,
                user = request.user
            )
            review.save()
            
            return redirect('/home/')          

        
    context = {
        'form': ReviewForm(initial={'ticket': ticket}) ,
        'ticket': ticket,        
        }        

    return render(request, 'feed/review_create.html', context=context)

@login_required
def review_detail(request, review_id):
    """ Review detail view """       
    review = Review.objects.get(id=review_id)
    ticket = Ticket.objects.get(id=review.ticket.id)
    
    context = {
        'review': review,
        'ticket': ticket,
        }          
    return render(request, 'feed/review_detail.html', context=context)


@login_required
def review_update(request, review_id):
    """ Update review """       
    review = Review.objects.get(id=review_id)
    post = review.ticket

    update_form = ReviewForm(instance=review)
    
    if request.method == 'POST':

        update_form = ReviewForm(request.POST, instance=review)
        if update_form.is_valid():
            update_form.save()
            return redirect('home')

    context = {
        'update_form': update_form,
        'review': review,
        'post': post,
        }
    
    return render(request, 'feed/review_update.html', context=context)


@login_required
def review_delete(request, review_id):
    """ Delete review """       
    review = Review.objects.get(id=review_id)
    if request.method == 'POST':
        review.delete()
        return redirect('home')
    return render(request, 'feed/review_delete.html', {'review': review})



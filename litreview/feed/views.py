from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.core.paginator import Paginator
from django.contrib import messages

from feed.models import Ticket, Review
from feed.forms import TicketForm, ReviewForm, TicketReviewForm
from authentication.models import UserFollow


@login_required
def home(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)

    followings = UserFollow.objects.filter(user=request.user)
    for following in followings:
        tickets = tickets | Ticket.objects.filter(user=following.followed_user)
        reviews = reviews | Review.objects.filter(user=following.followed_user)

    tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda x: x.time_created, reverse=True)

    p = Paginator(tickets_and_reviews, 5)
    page = request.GET.get('page')
    posts = p.get_page(page)

    reviews_ticket = [review.ticket for review in reviews]

    context = {
        'reviews_ticket': reviews_ticket,
        'posts': posts,
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

    p = Paginator(tickets_and_reviews, 5)
    page = request.GET.get('page')
    posts = p.get_page(page)

    reviews_ticket = [review.ticket for review in reviews]

    context = {
        'tickets': tickets,
        'reviews': reviews,
        'reviews_ticket': reviews_ticket,
        'posts': posts,
        }
    return render(request, 'feed/posts.html', context=context)


@login_required
def ticket_review_create(request):
    """ Create ticket & review """

    if request.method == 'POST':
        form = TicketReviewForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = Ticket(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                image=form.cleaned_data.get('image'),
                user=request.user
            )
            ticket.save()

            review = Review(
                headline=form.cleaned_data['headline'],
                rating=form.cleaned_data['rating'],
                body=form.cleaned_data['body'],
                ticket=ticket,
                user=request.user
            )
            review.save()
            messages.success(request, 'Votre ticket avec review a été crée.')
            return redirect('/home/')

    else:
        form = TicketReviewForm()

    context = {
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
            messages.success(request, 'Votre ticket a été crée.')
            return redirect('home')

    else:
        form = TicketForm()

    return render(request, 'feed/ticket_create.html', {'form': form})


@login_required
def ticket_update(request, ticket_id):
    """ Update Ticket """
    ticket = Ticket.objects.get(id=ticket_id)
    update_form = TicketForm(instance=ticket)
    
    context = {
        'update_form': update_form,
        'ticket': ticket,
        
        # 'form': ReviewForm(initial={'ticket': post}),
        
        }    

    if request.method == 'POST':
        update_form = TicketForm(request.POST, request.FILES, instance=ticket)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, 'Votre ticket a été mise à jour.')
            # return render(request, 'feed/home.html', context=context)
            return redirect('home')
            # return redirect('home')

    return render(request, 'feed/ticket_update.html', context=context)


@login_required
def ticket_delete(request, ticket_id):
    """ Delete Ticket """
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, 'Votre ticket a été supprimé.')
        return redirect('home')
    return render(request, 'feed/ticket_delete.html', {'ticket': ticket})


# REVIEW
@login_required
def review_create(request, ticket_id):
    """ Create a review for a ticket """

    post = Ticket.objects.get(id=ticket_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = Review(
                headline=form.cleaned_data['headline'],
                rating=form.cleaned_data['rating'],
                body=form.cleaned_data['body'],
                ticket=post,
                user=request.user
            )
            review.save()
            return redirect('/home/')

    context = {
        'form': ReviewForm(initial={'ticket': post}),
        'post': post,
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
            messages.success(request, 'Votre critique a été mise à jour')
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

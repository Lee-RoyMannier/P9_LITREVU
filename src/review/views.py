from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from tickets.forms import TicketForm
from . import forms
from tickets.models import Ticket

from .models import Review


# Create your views here.
@login_required
def create_review(request):
    review_form = forms.ReviewForm()
    ticket_form = TicketForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([review_form.is_valid(), ticket_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect("feed:home")
    return render(request, 'review/review_form.html', {'review_form': review_form,
                                                       "ticket_form": ticket_form})

@login_required
def respond_to_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect("feed:home")
    return render(request, 'review/review_ticket.html', {'review_form': review_form,
                                                         "ticket": ticket})


@login_required
def update_review(request, review_id):
    review = Review.objects.get(id=review_id)
    review_form = forms.ReviewForm(instance=review)
    ticket = review.ticket
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect("feed:home")
    return render(request, 'review/review_ticket.html', {'review_form': review_form,
                                                       "ticket":ticket})


@login_required
def delete_review(request, review_id):
    review = Review.objects.get(id=review_id)

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Your review has been deleted!')
        return redirect("feed:home")
    return render(request, 'review/delete_review.html', {'feed': review})

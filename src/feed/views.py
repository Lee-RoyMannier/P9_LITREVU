from itertools import chain

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from tickets.models import Ticket
from review.models import Review


@login_required
def home_page(request):
    context = {}
    ticket = Ticket.objects.filter(
        Q(user=request.user) |
        Q(user__in=request.user.following.values_list("followed_user", flat=True))
    )
    review = Review.objects.filter(
        Q(user=request.user) |
        Q(user__in=request.user.following.values_list("followed_user", flat=True))
    )
    sorted_models_chain = sorted(chain(ticket, review), key=lambda instance: instance.time_created,
                                 reverse=True)
    context['feeds'] = sorted_models_chain
    ratings = [1, 2, 3, 4, 5]
    context['ratings'] = ratings
    return render(request, 'feed/home_page.html', context=context)

@login_required
def my_post(request):
    my_feed_review = Review.objects.filter(user=request.user)
    my_feed_ticket = Ticket.objects.filter(user=request.user)

    my_feed = sorted(chain(my_feed_review, my_feed_ticket), key=lambda instance: instance.time_created,
                     reverse=True)
    ratings = [1, 2, 3, 4, 5]

    context = {'feeds': my_feed,
               "ratings": ratings}
    return render(request, 'feed/posts_feed.html', context=context)

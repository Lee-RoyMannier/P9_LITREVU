from django import template
from tickets.models import Ticket
from review.models import Review
register = template.Library()


@register.filter
def model_type(instance):
    return type(instance).__name__.lower()


@register.simple_tag(takes_context=True)
def post_by(context, user):
    if context['user'] == user:
        return 'vous'
    return user


@register.simple_tag
def can_create_review(ticket_id):
    return not Review.objects.filter(ticket=ticket_id).exists()


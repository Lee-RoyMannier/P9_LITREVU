from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms
from .models import Ticket


@login_required
def create_ticket(request):
    ticket_form = forms.TicketForm()
    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
        return redirect("feed:home")

    return render(request, 'tickets/ticket_form.html', {"ticket_form": ticket_form})


@login_required
def edit_ticket(request, id_ticket):
    ticket = Ticket.objects.get(id=id_ticket)
    ticket_form = forms.TicketForm(instance=ticket)

    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if ticket_form.is_valid():
            ticket_form.save()
            return redirect("feed:home")
    return render(request, 'tickets/ticket_form.html', {"ticket_form": ticket_form})


@login_required
def delete_ticket(request, id_ticket):
    ticket = Ticket.objects.get(id=id_ticket)
    if request.method == "POST":
        ticket.delete()
        return redirect("feed:home")
    return render(request, 'tickets/delete_ticket.html', {"feed": ticket})

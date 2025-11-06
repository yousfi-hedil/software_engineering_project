from django.shortcuts import render, redirect
from .models import Evenement
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import EvenementForm  


def liste_evenements(request):
    evenements = Evenement.objects.all()
    return render(request, "Evenement/list_event.html", {"liste": evenements})

def details_index(request):
    return redirect("liste_evenements")


class EvenementList(ListView):
    model = Evenement
    context_object_name = "liste"
    template_name = "Evenement/list_event.html"

class EvenementDetails(DetailView):
    model = Evenement
    template_name = "Evenement/detail_event.html"
    context_object_name = "evenement"

class EvenementCreate(CreateView):
    model = Evenement
    template_name = "Evenement/add_event.html"
    form_class = EvenementForm  
    success_url = reverse_lazy("liste_evenements")  

class EvenementUpdate(UpdateView):
    model = Evenement
    template_name = "Evenement/edit_event.html"
    form_class = EvenementForm
    success_url = reverse_lazy("liste_evenements")

class EvenementDelete(DeleteView):
    model = Evenement
    template_name = "Evenement/delete_event.html"
    success_url = reverse_lazy("liste_evenements")


from django.shortcuts import render, redirect
from .models import Evenement
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import EvenementForm  

# Front office
def volunteer(request):
    return render(request, "Evenement/volunteer.html")

def liste_evenements(request):
    evenements = Evenement.objects.all()
    return render(request, "Evenement/list_event.html", {"liste": evenements})

def details_index(request):
    return redirect("evenement:liste_evenements")  # Utiliser l'app_name

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
    success_url = reverse_lazy("evenement:liste_evenements")  

class EvenementUpdate(UpdateView):
    model = Evenement
    template_name = "Evenement/edit_event.html"
    form_class = EvenementForm
    success_url = reverse_lazy("evenement:liste_evenements")
    context_object_name = "evenement"

class EvenementDelete(DeleteView):
    model = Evenement
    template_name = "Evenement/delete_event.html"
    success_url = reverse_lazy("evenement:liste_evenements")
    context_object_name = "evenement"


# Back office / Administration
class EvenementListAdmin(ListView):
    model = Evenement
    template_name = "Evenement/admin_list_event.html"
    context_object_name = "liste"

class EvenementCreateAdmin(CreateView):
    model = Evenement
    form_class = EvenementForm
    template_name = "Evenement/admin_add_event.html"
    success_url = reverse_lazy("evenement:admin_evenements")  # correspond à l'URL de la liste admin

class EvenementUpdateAdmin(UpdateView):
    model = Evenement
    form_class = EvenementForm
    template_name = "Evenement/admin_add_event.html"
    success_url = reverse_lazy("evenement:admin_evenements")
    context_object_name = "evenement"

class EvenementDeleteAdmin(DeleteView):
    model = Evenement
    template_name = "Evenement/admin_delete_event.html"
    success_url = reverse_lazy("evenement:admin_evenements")
    context_object_name = "evenement"

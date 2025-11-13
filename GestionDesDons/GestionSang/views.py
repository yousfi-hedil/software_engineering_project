from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Sang
from .forms import SangForm


# ============================
# FRONT OFFICE
# ============================

class SangList(ListView):
    model = Sang
    template_name = 'sang/list_sang.html'
    context_object_name = 'sangs'


class SangDetails(DetailView):
    model = Sang
    template_name = 'sang/detail_sang.html'
    context_object_name = 'sang'


class SangCreate(CreateView):
    model = Sang
    form_class = SangForm
    template_name = 'sang/add_sang.html'
    # reverse vers le nom d'URL défini dans GestionSang/urls.py (inclus sans namespace)
    # Fallback to a concrete path to avoid reverse issues
    success_url = reverse_lazy('sang:liste_sangs')
    
    def form_valid(self, form):
        # debug log to confirm submission reached the view
        print(f"SangCreate.form_valid called; data={form.cleaned_data}")
        return super().form_valid(form)


class SangUpdate(UpdateView):
    model = Sang
    form_class = SangForm
    template_name = 'sang/edit_sang.html'
    success_url = reverse_lazy('sang:liste_sangs')
    def form_valid(self, form):
        print(f"SangUpdate.form_valid called; pk={self.get_object().pk}; data={form.cleaned_data}")
        return super().form_valid(form)


class SangDelete(DeleteView):
    model = Sang
    template_name = 'sang/delete_sang.html'
    success_url = reverse_lazy('sang:liste_sangs')
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        print(f"SangDelete.delete called; pk={obj.pk}")
        return super().delete(request, *args, **kwargs)


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')


class SangListAdmin(ListView):
    model = Sang
    # template présent dans GestionDesDons/Templates/Sang/admin_list_sang.html
    template_name = "Sang/admin_list_sang.html"
    context_object_name = "liste"



class SangCreateAdmin(CreateView):
    model = Sang
    form_class = SangForm
    template_name = "Sang/admin_add_sang.html"
    success_url = reverse_lazy('sang:admin_sangs')
    
    


class SangUpdateAdmin(UpdateView):
    model = Sang
    form_class = SangForm
    template_name = "Sang/admin_add_sang.html"  # même formulaire pour modif
    success_url = reverse_lazy('sang:admin_sangs') 

class SangDeleteAdmin(DeleteView):
    model = Sang
    # Correction du chemin du template (faute de frappe "ang" -> "Sang")
    template_name = "Sang/admin_delete_sang.html"
    success_url = reverse_lazy('sang:admin_sangs') 

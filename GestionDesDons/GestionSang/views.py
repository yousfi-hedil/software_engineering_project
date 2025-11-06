from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Sang
from .forms import SangForm 

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
    template_name = 'sang/add_sang.html'
    form_class = SangForm
    success_url = reverse_lazy('liste_sangs')



class SangUpdate(UpdateView):
    model = Sang
    template_name = 'sang/edit_sang.html'
    form_class = SangForm
    success_url = reverse_lazy('liste_sangs')

class SangDelete(DeleteView):
    model = Sang
    template_name = 'sang/delete_sang.html'
    success_url = reverse_lazy('liste_sangs')


from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

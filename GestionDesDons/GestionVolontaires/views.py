from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from .models import Volunteer
from .forms import VolunteerForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

app_name = 'volontaires'

# ✅ Liste des volontaires
def volunteer(request):
    qs = Volunteer.objects.all()
    q = (request.GET.get('q') or '').strip()
    spec = (request.GET.get('specialite') or '').strip()
    sort = (request.GET.get('sort') or 'date_recent').strip()

    if q:
        qs = qs.filter(
            models.Q(nom__icontains=q) |
            models.Q(prenom__icontains=q) |
            models.Q(specialite__icontains=q)
        )
    if spec:
        qs = qs.filter(specialite=spec)

    if sort == 'age_asc':
        qs = qs.order_by('age', '-date_inscription')
    elif sort == 'age_desc':
        qs = qs.order_by('-age', '-date_inscription')
    elif sort == 'date_ancien':
        qs = qs.order_by('date_inscription')
    else:  # date_recent (default)
        qs = qs.order_by('-date_inscription')

    ctx = {
        'volunteers': qs,
    }
    return render(request, 'volontaires/volunteer.html', ctx)
    # ⚠️ IMPORTANT : ton fichier existe sous ce nom, pas "volunteers_list.html"

# ✅ Ajouter un volontaire
def ajouter_volunteer(request):
    specialite = request.GET.get('specialite', '')
    
    if request.method == 'POST':
        form = VolunteerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('volontaires:liste_volunteers')
    else:
        # Pré-remplir le formulaire avec la spécialité si elle est fournie
        form = VolunteerForm(initial={'specialite': specialite} if specialite else None)

    return render(request, 'volontaires/ajout_volunteer.html', {
        'form': form,
        'errors': form.errors if request.method == 'POST' else None
    })
# ✅ Modifier un volontaire
def edit_volunteer(request, pk: int):
    obj = get_object_or_404(Volunteer, pk=pk)
    if request.method == 'POST':
        form = VolunteerForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('volontaires:liste_volunteers')  # Utilisez le bon nom d'URL
    else:
        form = VolunteerForm(instance=obj)
    return render(request, 'volontaires/ajout_volunteer.html', {'form': form})

# ✅ Supprimer un volontaire
def delete_volunteer(request, pk: int):
    obj = get_object_or_404(Volunteer, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('volontaires:liste_volunteers')  # Utilisez le bon nom d'URL
    return render(request, 'volontaires/supp_volanteer.html', {'volunteer': obj})

# ----------------------------
# ADMIN (back-office) views
# ----------------------------
class VolunteerListAdmin(ListView):
    model = Volunteer
    template_name = 'volontaires/admin_list_volunteer.html'
    context_object_name = 'liste'


class VolunteerCreateAdmin(CreateView):
    model = Volunteer
    form_class = VolunteerForm
    template_name = 'volontaires/admin_add_volunteer.html'
    success_url = reverse_lazy('volontaires:admin_volunteers') 
    
    def form_valid(self, form):
        print(f"VolunteerCreateAdmin.form_valid called: {form.cleaned_data}")
        return super().form_valid(form) 


class VolunteerUpdateAdmin(UpdateView):
    model = Volunteer
    form_class = VolunteerForm
    template_name = 'volontaires/admin_add_volunteer.html'
    success_url = reverse_lazy('volontaires:admin_volunteers') 
    context_object_name = 'volunteer'
    
    def form_valid(self, form):
        print(f"VolunteerUpdateAdmin.form_valid called for pk={self.get_object().pk}: {form.cleaned_data}")
        return super().form_valid(form)


class VolunteerDeleteAdmin(DeleteView):
    model = Volunteer
    template_name = 'volontaires/admin_delete_volunteer.html'
    success_url = reverse_lazy('volontaires:admin_volunteers') 
    context_object_name = 'volunteer'

from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from .models import Volunteer
from .forms import VolunteerForm

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
    if request.method == 'POST':
        form = VolunteerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('liste_volunteers')  # renvoie à la liste
    else:
        form = VolunteerForm()

    return render(request, 'volontaires/ajout_volunteer.html', {'form': form})
    # ⚠️ ton vrai fichier est bien "ajout_volunteer.html"

# ✅ Modifier un volontaire
def edit_volunteer(request, pk: int):
    obj = get_object_or_404(Volunteer, pk=pk)
    if request.method == 'POST':
        form = VolunteerForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('liste_volunteers')
    else:
        form = VolunteerForm(instance=obj)
    return render(request, 'volontaires/ajout_volunteer.html', {'form': form})
    # ✅ tu réutilises le même formulaire

# ✅ Supprimer un volontaire
def delete_volunteer(request, pk: int):
    obj = get_object_or_404(Volunteer, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('liste_volunteers')
    return render(request, 'volontaires/supp_volanteer.html', {'volunteer': obj})

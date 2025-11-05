from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from .models import Volunteer
from .forms import VolunteerForm

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

    specs = Volunteer.objects.exclude(specialite='').values_list('specialite', flat=True).distinct().order_by('specialite')

    total = qs.count()
    count_med = qs.filter(specialite='medecin').count()
    count_inf = qs.filter(specialite='infermier').count()
    count_psy = qs.filter(specialite='psychologue').count()
    count_h = qs.filter(sexe='homme').count()
    count_f = qs.filter(sexe='femme').count()

    ctx = {
        'volunteers': qs,
        'q': q,
        'current_spec': spec,
        'current_sort': sort,
        'specialites': specs,
        'stat_total': total,
        'stat_medecin': count_med,
        'stat_infermier': count_inf,
        'stat_psychologue': count_psy,
        'stat_homme': count_h,
        'stat_femme': count_f,
    }
    return render(request, 'volontaires/volunteer.html', ctx)

# CRUD VOLUNTEERS
def ajouter_volunteer(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('volunteer')
    else:
        initial = {}
        spec = (request.GET.get('specialite') or '').strip().lower()
        if spec in {'medecin', 'infermier', 'psychologue'}:
            initial['specialite'] = spec
        form = VolunteerForm(initial=initial)
    return render(request, 'volontaires/ajout_volunteer.html', {'form': form})

def edit_volunteer(request, pk: int):
    obj = get_object_or_404(Volunteer, pk=pk)
    if request.method == 'POST':
        form = VolunteerForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('volunteer')
    else:
        form = VolunteerForm(instance=obj)
    return render(request, 'volontaires/ajout_volunteer.html', {'form': form})

def delete_volunteer(request, pk: int):
    obj = get_object_or_404(Volunteer, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('volunteer')
    return render(request, 'volontaires/supp_volanteer.html', {'volunteer': obj})

from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.db.models import Count
from django.db.utils import OperationalError, ProgrammingError
from .models import BloodDonation, RefusedDonation
from .forms import BloodDonationForm

def donors(request):
    qs = BloodDonation.objects.all()
    q = (request.GET.get('q') or '').strip()
    group = (request.GET.get('group') or '').strip()
    sort = (request.GET.get('sort') or 'date_recent').strip()

    if q:
        qs = qs.filter(
            models.Q(nom__icontains=q) |
            models.Q(prenom__icontains=q) |
            models.Q(adresse__icontains=q)
        )
    if group:
        qs = qs.filter(blood_group=group)

    if sort == 'name_az':
        qs = qs.order_by('nom', 'prenom', '-created_at')
    elif sort == 'name_za':
        qs = qs.order_by('-nom', '-prenom', '-created_at')
    elif sort == 'date_ancien':
        qs = qs.order_by('created_at')
    else:  # date_recent
        qs = qs.order_by('-created_at')

    total_donations = qs.count()
    total_donors = qs.values('nom', 'prenom', 'mail').distinct().count()

    # Compute top group on the full dataset (not affected by current filters)
    top_group_row = (
        BloodDonation.objects.exclude(blood_group='')
          .values('blood_group')
          .annotate(c=Count('id'))
          .order_by('-c')
          .first()
    )
    stat_top_group_label = top_group_row['blood_group'] if top_group_row else '—'
    stat_top_group_count = top_group_row['c'] if top_group_row else 0

    try:
        stat_refused = RefusedDonation.objects.count()
    except (OperationalError, ProgrammingError):
        stat_refused = 0

    groups = BloodDonation.objects.exclude(blood_group='').values_list('blood_group', flat=True).distinct().order_by('blood_group')

    ctx = {
        'donations': qs,
        'stat_total_donations': total_donations,
        'stat_total_donors': total_donors,
        'stat_top_group_label': stat_top_group_label,
        'stat_top_group_count': stat_top_group_count,
        'stat_refused': stat_refused,
        'q': q,
        'current_group': group,
        'current_sort': sort,
        'groups': groups,
    }
    return render(request, 'doneurs/donors.html', ctx)

def ajouter_donors(request):
    if request.method == 'POST':
        form = BloodDonationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_donneurs')  # ← nouveau nom

        else:
            reasons = getattr(form, 'refusal_reasons', None)
            if reasons:
                try:
                    RefusedDonation.objects.create(
                        nom=request.POST.get('nom', ''),
                        prenom=request.POST.get('prenom', ''),
                        mail=request.POST.get('mail', ''),
                        telephone=request.POST.get('telephone', ''),
                        adresse=request.POST.get('adresse', ''),
                        blood_group=request.POST.get('blood_group', ''),
                        reasons=reasons,
                    )
                except (OperationalError, ProgrammingError):
                    pass
            # Re-render the form with validation errors
            return render(request, 'doneurs/ajout_aide.html', {'form': form})
    else:
        form = BloodDonationForm()
    return render(request, 'doneurs/ajout_aide.html', {'form': form})

def edit_donor(request, pk: int):
    obj = get_object_or_404(BloodDonation, pk=pk)
    if request.method == 'POST':
        form = BloodDonationForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('liste_donneurs')
    else:
        form = BloodDonationForm(instance=obj)
    return render(request, 'doneurs/ajout_aide.html', {'form': form})

def delete_donor(request, pk: int):
    obj = get_object_or_404(BloodDonation, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('liste_donneurs')
    return render(request, 'doneurs/supp_donors.html', {'donation': obj})

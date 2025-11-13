from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.db.models import Count
from django.db.utils import OperationalError, ProgrammingError
from .models import BloodDonation, RefusedDonation
from .forms import BloodDonationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect

# ----------------------------
# PUBLIC / FRONT-END VIEWS
# ----------------------------

def donors(request):
    """
    Liste publique des donateurs.
    """
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

    top_group_row = (
        BloodDonation.objects.exclude(blood_group='').values('blood_group')
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

    context = {
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
    return render(request, 'doneurs/donors.html', context)


# ----------------------------
# FRONT-END DONOR CRUD
# ----------------------------
def ajouter_donors(request):
    """
    Vue front-end pour ajouter un donateur (pas d'interface admin).
    """
    if request.method == 'POST':
        form = BloodDonationForm(request.POST)
        if form.is_valid():
            saved = form.save()
            # si le formulaire a des raisons de refus, afficher le formulaire avec les motifs
            if getattr(form, 'refusal_reasons', None):
                return render(request, 'doneurs/ajouter_donors.html', {'form': form, 'refused': True, 'reasons': form.refusal_reasons})
            return redirect('doneurs:liste_donneurs')  # retour vers la liste front
    else:
        form = BloodDonationForm()

    return render(request, 'doneurs/ajouter_donors.html', {'form': form})



def edit_donor(request, pk):
    """
    Éditer un donateur côté front-end.
    """
    obj = get_object_or_404(BloodDonation, pk=pk)
    if request.method == 'POST':
        form = BloodDonationForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('doneurs:liste_donneurs')
    else:
        form = BloodDonationForm(instance=obj)

    return render(request, 'doneurs/ajouter_donors.html', {'form': form, 'donation': obj})


def delete_donor(request, pk: int):
    """
    Supprimer un donateur côté front-end.
    """
    obj = get_object_or_404(BloodDonation, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('doneurs:liste_donneurs')
    # render the existing 'supp_donors.html' confirmation template
    return render(request, 'doneurs/supp_donors.html', {'donation': obj})


# ----------------------------
# ADMIN (BACK-OFFICE) VIEWS
# ----------------------------

class DonorListAdmin(ListView):
    model = BloodDonation
    template_name = 'doneurs/admin_list_donors.html'
    context_object_name = 'liste'


class DonorCreateAdmin(CreateView):
    model = BloodDonation
    form_class = BloodDonationForm
    template_name = 'doneurs/admin_add_donor.html'
    success_url = reverse_lazy('doneurs:admin_donors')

    def form_valid(self, form):
        saved = form.save()
        if getattr(form, 'refusal_reasons', None):
            # render same template showing reasons and do not redirect/save a BloodDonation
            return self.render_to_response(self.get_context_data(form=form, refused=True, reasons=form.refusal_reasons))
        # normal flow
        self.object = saved
        return HttpResponseRedirect(self.get_success_url())


class DonorUpdateAdmin(UpdateView):
    model = BloodDonation
    form_class = BloodDonationForm
    template_name = 'doneurs/admin_add_donor.html'
    success_url = reverse_lazy('doneurs:admin_donors')
    context_object_name = 'donation'


class DonorDeleteAdmin(DeleteView):
    model = BloodDonation
    template_name = 'doneurs/admin_delete_donor.html'
    success_url = reverse_lazy('doneurs:admin_donors')
    context_object_name = 'donation'

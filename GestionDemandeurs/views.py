from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Demandeur
from .forms import DemandeurForm

# Add a new demandeur
def add_demandeur(request):
    if request.method == 'POST':
        form = DemandeurForm(request.POST, request.FILES)
        if form.is_valid():
            demandeur = form.save()
            messages.success(request, f"Demandeur {demandeur.nom_user} {demandeur.prenom_user} ajouté avec succès!")
            return redirect('list_demandeur')
        else:
            messages.error(request, "Erreur lors de l'ajout du demandeur. Veuillez vérifier les informations.")
    else:
        form = DemandeurForm()
    
    return render(request, 'GestionDemandeurs/add_demandeur.html', {'form': form})

# List all demandeurs
def list_demandeur(request):
    demandeurs = Demandeur.objects.all()
    search = request.GET.get('search')
    if search:
        demandeurs = demandeurs.filter(nom_user__icontains=search) | demandeurs.filter(prenom_user__icontains=search)
    
    return render(request, 'GestionDemandeurs/list_demandeur.html', {'demandeurs': demandeurs})

# Detail of a single demandeur
def detail_demandeur(request, pk):
    demandeur = get_object_or_404(Demandeur, pk=pk)
    return render(request, 'GestionDemandeurs/detail_demandeur.html', {'demandeur': demandeur})

# Edit demandeur
def edit_demandeur(request, pk):
    demandeur = get_object_or_404(Demandeur, pk=pk)
    if request.method == 'POST':
        form = DemandeurForm(request.POST, request.FILES, instance=demandeur)
        if form.is_valid():
            form.save()
            messages.success(request, "Demandeur modifié avec succès!")
            return redirect('detail_demandeur', pk=demandeur.pk)
        else:
            messages.error(request, "Erreur lors de la modification.")
    else:
        form = DemandeurForm(instance=demandeur)
    return render(request, 'GestionDemandeurs/edit_demandeur.html', {'form': form, 'demandeur': demandeur})

# Delete demandeur
def delete_demandeur(request, pk):
    demandeur = get_object_or_404(Demandeur, pk=pk)
    if request.method == 'POST':
        nom = f"{demandeur.nom_user} {demandeur.prenom_user}"
        demandeur.delete()
        messages.success(request, f"Demandeur {nom} supprimé avec succès!")
        return redirect('list_demandeur')
    return render(request, 'GestionDemandeurs/delete_demandeur.html', {'demandeur': demandeur})

# Show all demandeurs at /demandeurs/detail/
def all_demandeurs(request):
    demandeurs = Demandeur.objects.all()
    return render(request, 'GestionDemandeurs/all_demandeurs.html', {'demandeurs': demandeurs})

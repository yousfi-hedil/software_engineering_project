#!/usr/bin/env python
"""Test script to verify volunteer admin CRUD views work correctly."""
import os
import sys
import django

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GestionDesDons.settings')
sys.path.insert(0, '/Users/Hejer/Desktop/crud-4-template - Copie/GestionDesDons')
django.setup()

from django.test import Client
from django.urls import reverse
from GestionVolontaires.models import Volunteer

client = Client()

# Test 1: GET the admin add form
print("Test 1: GET admin add volunteer form...")
try:
    response = client.get(reverse('volontaires:admin_volunteer_add'))
    print(f"  Status: {response.status_code} (expect 200)")
    if response.status_code == 200:
        print("  ✓ Form GET successful")
    else:
        print(f"  ✗ Unexpected status {response.status_code}")
        print(f"    Content: {response.content[:200]}")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 2: POST to create a volunteer
print("\nTest 2: POST to create volunteer...")
data = {
    'nom': 'TestNom',
    'prenom': 'TestPrenom',
    'email': 'test@example.com',
    'telephone': '0123456789',
    'ville': 'Paris',
    'adresse': '123 Rue de Test',
    'age': 30,
    'sexe': 'homme',
    'disponibilite': 'matin',
    'specialite': 'medecin',
}
try:
    response = client.post(reverse('volontaires:admin_volunteer_add'), data)
    print(f"  Status: {response.status_code}")
    if response.status_code == 302:
        print("  ✓ POST redirected (expected after successful save)")
        # Check if volunteer was created
        created = Volunteer.objects.filter(nom='TestNom', prenom='TestPrenom').exists()
        if created:
            print("  ✓ Volunteer created in database")
        else:
            print("  ✗ Volunteer NOT found in database")
    else:
        print(f"  Response content (first 500 chars):")
        print(f"    {response.content[:500]}")
except Exception as e:
    print(f"  ✗ Error: {e}")

print("\nTest complete.")

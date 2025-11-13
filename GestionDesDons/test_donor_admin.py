#!/usr/bin/env python
"""Quick test script to exercise the Donor admin create view via Django test client.
Run from project root with the virtualenv activated.
"""
import os
import sys

proj_root = r"c:\Users\Hejer\Desktop\crud-4-template - Copie\GestionDesDons"
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GestionDesDons.settings')

import django
from django.test import Client
from django.urls import reverse

django.setup()

client = Client()

print("GET admin add donor page...")
try:
    resp = client.get(reverse('doneurs:admin_donor_add'))
    print('Status:', resp.status_code)
    if resp.status_code == 200:
        print('Form page OK')
    else:
        print(resp.content[:400])
except Exception as e:
    print('GET error:', e)

print('\nPOST create donor...')
data = {
    'nom': 'TestNom',
    'prenom': 'TestPrenom',
    'mail': 'test@example.com',
    'telephone': '12345678',
    'adresse': '1 Rue Test',
    'ville': 'Casablanca',
    'poids': '60.0',
    'blood_group': 'A+',
    'traitement_medical': 'False',
    'maladie_chronique': 'False',
    'antecedents_recents': ['aucun'],
    'date_naissance': '1990-01-01',
}
try:
    resp = client.post(reverse('doneurs:admin_donor_add'), data)
    print('Status after POST:', resp.status_code)
    if resp.status_code in (301, 302):
        print('Redirected - likely success')
    else:
        print('Response content snippet:')
        print(resp.content[:800])
except Exception as e:
    print('POST error:', e)

print('\nDone')

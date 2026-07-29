#!/bin/bash
echo "=== La Une Multiservice — Installation ==="
pip install django pillow
python manage.py makemigrations core blog devis
python manage.py migrate
python manage.py createsuperuser --username admin --email admin@launemultiservice.com
python manage.py loaddata initial_data.json 2>/dev/null || echo "(pas de fixtures initiales)"
echo ""
echo "=== Démarrage du serveur ==="
python manage.py runserver

# 🏢 La Une Multiservice — Site Web Django

Site web complet pour **La Une Multiservice** — entreprise multi-services (Architecture, Informatique, Plomberie, Électricité, Construction, Climatisation).

## ✨ Pages incluses

| Page | URL | Description |
|------|-----|-------------|
| Accueil | `/` | Hero animé, services, stats, projets, témoignages, blog |
| Services | `/services/` | Liste de tous les domaines |
| Détail service | `/services/<slug>/` | Page dédiée par domaine + FAQ + projets |
| Portfolio | `/portfolio/` | Filtrable par domaine |
| Détail projet | `/portfolio/<slug>/` | Fiche projet complète |
| À Propos | `/a-propos/` | Mission, valeurs, équipe, timeline |
| Contact | `/contact/` | Formulaire + carte |
| Devis en ligne | `/devis/` | Formulaire multi-étapes |
| Blog | `/blog/` | Articles filtrables |
| Détail article | `/blog/<slug>/` | Article complet |
| FAQ | `/faq/` | Accordion filtrable par domaine |
| Témoignages | `/temoignages/` | Avis clients filtrables |
| Admin | `/admin/` | Gestion complète du contenu |
| Connexion | `/auth/login/` | Accès admin |

## 🚀 Installation

### Prérequis
- Python 3.10+
- pip

### Démarrage rapide

```bash
# 1. Installer les dépendances
pip install django pillow

# 2. Migrations
python manage.py makemigrations core blog devis
python manage.py migrate

# 3. Créer le super admin
python manage.py createsuperuser

# 4. Charger les données initiales (services, stats, témoignages, FAQ)
python manage.py loaddata initial_data.json

# 5. Lancer le serveur
python manage.py runserver
```

Accédez à `http://127.0.0.1:8000` pour le site et `http://127.0.0.1:8000/admin` pour l'administration.

## 🎨 Design System

- **Couleurs :** Bleu nuit `#0D1B2A` · Or `#C9A84C` · Crème `#F8F5EE`
- **Typographie :** Playfair Display (titres) + Inter (corps)
- **CSS :** Pur CSS sans framework, entièrement responsive

## ⚙️ Fonctionnalités Admin

Le super admin peut :
- Publier/dépublier des **articles de blog** avec illustrations
- Gérer les **domaines de services** et leurs fonctionnalités
- Gérer les **projets du portfolio** avec photos
- Gérer les **témoignages clients**
- Gérer les **membres de l'équipe**
- Consulter et traiter les **messages de contact**
- Consulter et traiter les **demandes de devis**
- Gérer les **FAQ** par domaine
- Gérer les **statistiques** affichées

## 📁 Structure

```
laune_multiservice/
├── core/           # App principale (services, projets, équipe, FAQ)
├── blog/           # App blog & actualités
├── devis/          # App demandes de devis
├── static/
│   ├── css/main.css
│   └── js/main.js
├── templates/
│   ├── base.html
│   ├── core/
│   ├── blog/
│   └── devis/
├── media/          # Uploads (créé automatiquement)
├── initial_data.json
└── manage.py
```

## 🆕 Nouvelles fonctionnalités (v2)

### 🖼️ Galerie multi-photos
- Modèle `ProjectPhoto` : autant de photos que voulu par projet
- Modèle `CataloguePhoto` : galerie sur les fiches catalogue
- Lightbox fullscreen avec navigation clavier (← →) et swipe
- Grille en mosaïque avec grande image principale

### 💬 Chat en ligne
- Widget flottant doré en bas à droite
- Bot automatique avec 15+ réponses contextuelles (devis, services, horaires, urgences...)
- Badge de notification après 8 secondes
- Historique de session persistant
- Vue admin des conversations : `/chat/admin-view/`

### 📦 Catalogue produits & services
- 3 types : Prestation, Produit, Pack
- Prix en FCFA avec unités configurables
- Filtre par catégorie, domaine, type, recherche texte
- Fiche détaillée avec galerie, prix, garantie, liste d'inclus
- Page : `/catalogue/`

### ✨ Animations premium
- **Curseur personnalisé doré** avec follower fluide
- **Particules canvas** connectées sur le hero
- **Typewriter** sur le titre hero (cycle des domaines)
- **Tilt 3D** au hover sur les cartes (avec reflet lumineux)
- **Boutons magnétiques** qui suivent le curseur
- **Page transitions** overlay LU entre les pages
- **Texte gradient animé** en mouvement continu
- **Scroll indicator** animé sur le hero
- **Compteurs easing** cubique au scroll
- **Navbar intelligente** qui se cache/réapparaît au scroll
- **Barre de progression** de lecture en haut
- **Ripple doré** au clic sur les boutons
- **Lignes dorées** qui s'étendent au scroll
- **Pulse lumineux** sur les statistiques

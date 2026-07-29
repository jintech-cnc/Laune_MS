import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import ChatSession, ChatMessage


# ── Bot auto-responses ──────────────────────────────────────────────────
BOT_RESPONSES = {
    'bonjour': "Bonjour et bienvenue chez **La Une Multiservice** ! 👋\nComment puis-je vous aider aujourd'hui ?\n\n• Services & Prestations\n• Demander un devis\n• Nos réalisations\n• Horaires & Contact",
    'salut': "Salut ! Bienvenue chez La Une Multiservice 😊 En quoi puis-je vous aider ?",
    'bonjour comment': "Bonjour ! Je vais très bien, merci. Et vous ? Comment puis-je vous aider aujourd'hui ?",
    'devis': "Pour un **devis gratuit**, vous pouvez :\n\n1️⃣ Remplir notre formulaire en ligne → [Demander un devis](/devis/)\n2️⃣ Nous appeler au **+237 6XX XXX XXX**\n3️⃣ Écrire à **devis@launemultiservice.com**\n\nNous vous répondons sous **24 heures** ! ⚡",
    'prix': "Nos tarifs varient selon le type de projet. Consultez notre **catalogue** pour une idée des prix, ou demandez un **devis gratuit** pour une estimation précise.\n\n👉 [Voir le catalogue](/catalogue/)\n👉 [Demander un devis](/devis/)",
    'tarif': "Nos tarifs sont disponibles dans notre catalogue en ligne. Certaines prestations sont sur devis selon la complexité du projet.\n\n👉 [Voir le catalogue](/catalogue/)",
    'architecture': "Notre pôle **Architecture** propose :\n\n🏛️ Plans & conception architecturale\n🏠 Construction neuve & extension\n🎨 Décoration intérieure\n📋 Permis de construire\n\n👉 [En savoir plus](/services/architecture/)",
    'informatique': "Notre pôle **Informatique** propose :\n\n💻 Développement web & mobile\n🌐 Infrastructure réseau\n🔒 Cybersécurité\n🖥️ Maintenance & support\n\n👉 [En savoir plus](/services/informatique/)",
    'plomberie': "Notre service **Plomberie** couvre :\n\n🔧 Installation sanitaire\n💧 Détection & réparation de fuites\n🚿 Chauffe-eau & chauffe-bain\n⚡ Dépannage d'urgence 24h/7j\n\n👉 [En savoir plus](/services/plomberie/)",
    'electricite': "Notre service **Électricité** propose :\n\n⚡ Câblage & tableau électrique\n☀️ Panneaux solaires\n💡 Éclairage intérieur/extérieur\n🔋 Onduleurs & groupes électrogènes\n\n👉 [En savoir plus](/services/electricite/)",
    'urgence': "Pour une **urgence**, appelez-nous directement :\n\n📞 **+237 6XX XXX XXX** (disponible 24h/7j)\n\nNos équipes interviennent sous **2 à 4 heures** pour les urgences plomberie et électricité.",
    'horaire': "Nos horaires d'ouverture :\n\n🕗 **Lundi — Vendredi** : 8h00 — 18h00\n🕘 **Samedi** : 9h00 — 14h00\n\nPour les urgences, notre hotline est disponible **24h/7j**.",
    'contact': "Vous pouvez nous joindre via :\n\n📍 **Adresse** : Yaoundé, Cameroun — Quartier Bastos\n📞 **Téléphone** : +237 6XX XXX XXX\n✉️ **E-mail** : contact@launemultiservice.com\n\n👉 [Formulaire de contact](/contact/)",
    'portfolio': "Découvrez nos réalisations sur notre page Portfolio !\n\n🏗️ Plus de 500 projets réalisés en 14 ans.\n\n👉 [Voir le portfolio](/portfolio/)",
    'merci': "Avec plaisir ! 😊 N'hésitez pas si vous avez d'autres questions. Bonne journée !",
    'au revoir': "Au revoir ! Bonne journée 👋 N'hésitez pas à revenir si vous avez besoin d'aide.",
    'garantie': "Oui, tous nos travaux sont garantis :\n\n🛡️ **2 ans** pour les installations\n🛡️ **5 ans** pour le gros œuvre\n\nNous proposons aussi des **contrats de maintenance** annuels.",
    'delai': "Les délais dépendent du type de projet :\n\n⚡ Urgences : 2 à 4 heures\n🔧 Petits travaux : 1 à 3 jours\n🏗️ Projets importants : planning défini avec vous\n\nDemandez un devis pour un délai précis.",
}

DEFAULT_RESPONSE = "Je n'ai pas bien compris votre question. 🤔\n\nVoici ce que je peux faire pour vous :\n\n• **Devis** — Obtenir un devis gratuit\n• **Services** — Nos prestations\n• **Contact** — Nous joindre\n• **Urgence** — Intervention rapide\n\nOu tapez votre question et un membre de notre équipe vous répondra dès que possible !"


def get_bot_response(text):
    text_lower = text.lower().strip()
    # Exact or partial keyword match
    for keyword, response in BOT_RESPONSES.items():
        if keyword in text_lower:
            return response
    return DEFAULT_RESPONSE


# ── Views ───────────────────────────────────────────────────────────────

def get_or_create_session(request):
    session_id = request.session.get('chat_session_id')
    if session_id:
        try:
            return ChatSession.objects.get(session_id=session_id)
        except ChatSession.DoesNotExist:
            pass
    session = ChatSession.objects.create()
    request.session['chat_session_id'] = str(session.session_id)
    return session


@require_POST
def send_message(request):
    try:
        data = json.loads(request.body)
        content = data.get('message', '').strip()
        visitor_name = data.get('name', '').strip()
        visitor_email = data.get('email', '').strip()

        if not content:
            return JsonResponse({'error': 'Message vide'}, status=400)

        session = get_or_create_session(request)

        # Update visitor info if provided
        if visitor_name:
            session.visitor_name = visitor_name
        if visitor_email:
            session.visitor_email = visitor_email
        session.save()

        # Save visitor message
        ChatMessage.objects.create(
            session=session,
            sender='visitor',
            content=content,
        )

        # Bot auto-response
        bot_reply = get_bot_response(content)
        bot_msg = ChatMessage.objects.create(
            session=session,
            sender='bot',
            content=bot_reply,
        )

        return JsonResponse({
            'status': 'ok',
            'bot_reply': bot_reply,
            'timestamp': bot_msg.sent_at.strftime('%H:%M'),
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_history(request):
    session = get_or_create_session(request)
    messages = session.messages.all().order_by('sent_at')
    return JsonResponse({
        'messages': [
            {
                'sender': m.sender,
                'content': m.content,
                'timestamp': m.sent_at.strftime('%H:%M'),
            }
            for m in messages
        ]
    })


def chat_admin_view(request):
    """Admin view to see all chat sessions"""
    sessions = ChatSession.objects.prefetch_related('messages').order_by('-last_activity')[:50]
    return render(request, 'chat/admin_chat.html', {'sessions': sessions})

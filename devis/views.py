from django.shortcuts import render, redirect
from django.contrib import messages
from .models import DemandeDevis
from core.models import ServiceDomain


def devis_request(request):
    services = ServiceDomain.objects.filter(is_active=True)
    if request.method == 'POST':
        domain_id = request.POST.get('domain')
        domain = None
        if domain_id:
            try:
                domain = ServiceDomain.objects.get(id=domain_id)
            except ServiceDomain.DoesNotExist:
                pass
        DemandeDevis.objects.create(
            name=request.POST.get('name', ''),
            email=request.POST.get('email', ''),
            phone=request.POST.get('phone', ''),
            company=request.POST.get('company', ''),
            domain=domain,
            project_title=request.POST.get('project_title', ''),
            description=request.POST.get('description', ''),
            location=request.POST.get('location', ''),
            budget=request.POST.get('budget', 'undefined'),
            urgency=request.POST.get('urgency', 'flexible'),
            attachment=request.FILES.get('attachment'),
        )
        messages.success(request, "Votre demande de devis a bien été reçue ! Notre équipe vous contactera dans les 24 heures.")
        return redirect('devis_success')
    return render(request, 'devis/request.html', {'services': services})


def devis_success(request):
    return render(request, 'devis/success.html')

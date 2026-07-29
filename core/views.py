from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import ServiceDomain, Project, Testimonial, TeamMember, ContactMessage, FAQ, Statistic
from blog.models import Article


def home(request):
    services = ServiceDomain.objects.filter(is_active=True)[:6]
    featured_projects = Project.objects.filter(is_featured=True)[:6]
    testimonials = Testimonial.objects.filter(is_featured=True)[:4]
    stats = Statistic.objects.all()
    recent_articles = Article.objects.filter(is_published=True).order_by('-published_at')[:3]
    context = {
        'services': services,
        'featured_projects': featured_projects,
        'testimonials': testimonials,
        'stats': stats,
        'recent_articles': recent_articles,
    }
    return render(request, 'core/home.html', context)


def about(request):
    team = TeamMember.objects.filter(is_active=True)
    stats = Statistic.objects.all()
    context = {'team': team, 'stats': stats}
    return render(request, 'core/about.html', context)


def contact(request):
    services = ServiceDomain.objects.filter(is_active=True)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()
        domain_id = request.POST.get('domain')
        domain = None
        if domain_id:
            try:
                domain = ServiceDomain.objects.get(id=domain_id)
            except ServiceDomain.DoesNotExist:
                pass
        if name and email and subject and message_text:
            ContactMessage.objects.create(
                name=name, email=email, phone=phone,
                subject=subject, message=message_text, domain=domain
            )
            messages.success(request, "Votre message a bien été envoyé. Nous vous répondrons dans les plus brefs délais.")
            return redirect('contact')
        else:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
    return render(request, 'core/contact.html', {'services': services})


def service_detail(request, slug):
    service = get_object_or_404(ServiceDomain, slug=slug, is_active=True)
    projects = service.projects.all()[:6]
    faqs = service.faq_set.filter(is_active=True)
    context = {'service': service, 'projects': projects, 'faqs': faqs}
    return render(request, 'core/service_detail.html', context)


def services_list(request):
    services = ServiceDomain.objects.filter(is_active=True)
    return render(request, 'core/services_list.html', {'services': services})


def portfolio(request):
    services = ServiceDomain.objects.filter(is_active=True)
    domain_slug = request.GET.get('domain')
    projects = Project.objects.select_related('domain')
    if domain_slug:
        projects = projects.filter(domain__slug=domain_slug)
    active_domain = domain_slug
    context = {'projects': projects, 'services': services, 'active_domain': active_domain}
    return render(request, 'core/portfolio.html', context)


def faq(request):
    services = ServiceDomain.objects.filter(is_active=True)
    domain_slug = request.GET.get('domain')
    faqs = FAQ.objects.filter(is_active=True).select_related('domain')
    if domain_slug:
        faqs = faqs.filter(domain__slug=domain_slug)
    general_faqs = FAQ.objects.filter(is_active=True, domain__isnull=True)
    context = {
        'faqs': faqs,
        'general_faqs': general_faqs,
        'services': services,
        'active_domain': domain_slug,
    }
    return render(request, 'core/faq.html', context)


def testimonials_page(request):
    testimonials = Testimonial.objects.all().select_related('domain')
    services = ServiceDomain.objects.filter(is_active=True)
    domain_slug = request.GET.get('domain')
    if domain_slug:
        testimonials = testimonials.filter(domain__slug=domain_slug)
    context = {'testimonials': testimonials, 'services': services, 'active_domain': domain_slug}
    return render(request, 'core/testimonials.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related = Project.objects.filter(domain=project.domain).exclude(pk=project.pk)[:3]
    return render(request, 'core/project_detail.html', {'project': project, 'related': related})

from django.shortcuts import render, get_object_or_404
from .models import CatalogueItem, CatalogueCategory
from core.models import ServiceDomain


def catalogue_list(request):
    items = CatalogueItem.objects.filter(is_active=True).select_related('category', 'domain')
    categories = CatalogueCategory.objects.filter(is_active=True)
    services = ServiceDomain.objects.filter(is_active=True)

    # Filters
    cat_slug = request.GET.get('category')
    domain_slug = request.GET.get('domain')
    item_type = request.GET.get('type')
    search = request.GET.get('q', '')

    if cat_slug:
        items = items.filter(category__slug=cat_slug)
    if domain_slug:
        items = items.filter(domain__slug=domain_slug)
    if item_type:
        items = items.filter(item_type=item_type)
    if search:
        items = items.filter(name__icontains=search) | items.filter(short_description__icontains=search)

    featured = CatalogueItem.objects.filter(is_active=True, is_featured=True)[:4]

    context = {
        'items': items,
        'categories': categories,
        'services': services,
        'featured': featured,
        'active_cat': cat_slug,
        'active_domain': domain_slug,
        'active_type': item_type,
        'search': search,
        'type_choices': CatalogueItem.TYPE_CHOICES,
    }
    return render(request, 'boutique/list.html', context)


def catalogue_detail(request, slug):
    item = get_object_or_404(CatalogueItem, slug=slug, is_active=True)
    related = CatalogueItem.objects.filter(
        is_active=True, domain=item.domain
    ).exclude(pk=item.pk)[:4]
    context = {'item': item, 'related': related}
    return render(request, 'boutique/detail.html', context)

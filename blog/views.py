from django.shortcuts import render, get_object_or_404
from .models import Article, Category
from core.models import ServiceDomain


def blog_list(request):
    articles = Article.objects.filter(is_published=True)
    category_slug = request.GET.get('category')
    domain_slug = request.GET.get('domain')
    search = request.GET.get('q', '')
    categories = Category.objects.all()
    services = ServiceDomain.objects.filter(is_active=True)
    if category_slug:
        articles = articles.filter(category__slug=category_slug)
    if domain_slug:
        articles = articles.filter(domain__slug=domain_slug)
    if search:
        articles = articles.filter(title__icontains=search) | articles.filter(content__icontains=search)
    featured = articles.filter(is_featured=True).first()
    context = {
        'articles': articles,
        'featured': featured,
        'categories': categories,
        'services': services,
        'search': search,
        'active_category': category_slug,
        'active_domain': domain_slug,
    }
    return render(request, 'blog/list.html', context)


def blog_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    article.views_count += 1
    article.save(update_fields=['views_count'])
    related = Article.objects.filter(is_published=True, domain=article.domain).exclude(pk=article.pk)[:3]
    context = {'article': article, 'related': related}
    return render(request, 'blog/detail.html', context)

from django.db import models
from django.utils.text import slugify
from core.models import ServiceDomain


class CatalogueCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True, default='📦')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Catégorie catalogue'
        verbose_name_plural = 'Catégories catalogue'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CatalogueItem(models.Model):
    TYPE_CHOICES = [
        ('service', 'Prestation de service'),
        ('product', 'Produit / Matériel'),
        ('pack', 'Pack / Offre groupée'),
    ]
    UNIT_CHOICES = [
        ('unit', 'Unité'),
        ('m2', 'm²'),
        ('ml', 'Mètre linéaire'),
        ('hour', 'Heure'),
        ('day', 'Jour'),
        ('forfait', 'Forfait'),
        ('lot', 'Lot'),
    ]

    item_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='service', verbose_name='Type')
    category = models.ForeignKey(CatalogueCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    domain = models.ForeignKey(ServiceDomain, on_delete=models.SET_NULL, null=True, blank=True, related_name='catalogue_items')
    name = models.CharField(max_length=200, verbose_name='Nom')
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=300, verbose_name='Description courte')
    description = models.TextField(verbose_name='Description détaillée')
    cover_image = models.ImageField(upload_to='catalogue/', blank=True, null=True, verbose_name='Image principale')

    # Pricing
    price = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True, verbose_name='Prix (FCFA)')
    price_unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='forfait', verbose_name='Unité de prix')
    price_on_quote = models.BooleanField(default=False, verbose_name='Prix sur devis')
    price_from = models.BooleanField(default=False, verbose_name='À partir de')

    # Specs
    duration = models.CharField(max_length=100, blank=True, verbose_name='Durée / Délai')
    warranty = models.CharField(max_length=100, blank=True, verbose_name='Garantie')
    includes = models.TextField(blank=True, verbose_name='Ce qui est inclus (une ligne = un élément)')

    # Status
    is_active = models.BooleanField(default=True, verbose_name='Actif')
    is_featured = models.BooleanField(default=False, verbose_name='Mis en avant')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Article catalogue'
        verbose_name_plural = 'Articles catalogue'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.get_item_type_display()}] {self.name}"

    def get_price_display(self):
        if self.price_on_quote:
            return "Sur devis"
        if self.price:
            prefix = "À partir de " if self.price_from else ""
            return f"{prefix}{int(self.price):,} FCFA / {self.get_price_unit_display()}".replace(',', ' ')
        return "Nous contacter"

    def get_includes_list(self):
        if self.includes:
            return [line.strip() for line in self.includes.splitlines() if line.strip()]
        return []


class CataloguePhoto(models.Model):
    item = models.ForeignKey(CatalogueItem, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='catalogue/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Photo — {self.item.name}"

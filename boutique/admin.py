from django.contrib import admin
from .models import CatalogueCategory, CatalogueItem, CataloguePhoto


class CataloguePhotoInline(admin.TabularInline):
    model = CataloguePhoto
    extra = 3
    fields = ['image', 'caption', 'order']


@admin.register(CatalogueCategory)
class CatalogueCategoryAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(CatalogueItem)
class CatalogueItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'item_type', 'category', 'domain', 'get_price_display', 'is_featured', 'is_active', 'order']
    list_editable = ['is_featured', 'is_active', 'order']
    list_filter = ['item_type', 'category', 'domain', 'is_featured', 'is_active', 'price_on_quote']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'short_description', 'description']
    inlines = [CataloguePhotoInline]
    fieldsets = (
        ('Informations générales', {
            'fields': ('item_type', 'category', 'domain', 'name', 'slug', 'short_description', 'description', 'cover_image')
        }),
        ('Tarification', {
            'fields': ('price', 'price_unit', 'price_on_quote', 'price_from')
        }),
        ('Détails techniques', {
            'fields': ('duration', 'warranty', 'includes')
        }),
        ('Publication', {
            'fields': ('is_active', 'is_featured', 'order')
        }),
    )

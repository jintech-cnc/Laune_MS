from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ServiceDomain, ServiceFeature, Project, ProjectPhoto,
    Testimonial, TeamMember, ContactMessage, FAQ, Statistic
)


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 2
    fields = ['title', 'description', 'order']


class ProjectPhotoInline(admin.TabularInline):
    model = ProjectPhoto
    extra = 3
    fields = ['image', 'caption', 'order']


@admin.register(ServiceDomain)
class ServiceDomainAdmin(admin.ModelAdmin):
    class Media:
        css = {'all': ('css/admin_custom.css',)}

    list_display  = ['cover_thumb', 'name', 'tagline', 'order', 'is_active']
    list_display_links = ['cover_thumb', 'name']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    inlines       = [ServiceFeatureInline]
    list_filter   = ['is_active']
    search_fields = ['name', 'description']

    fieldsets = (
        ('🖼️  Image de couverture', {
            'description': 'Uploadez une image représentative de ce service. Elle sera affichée sur la carte et la page du service.',
            'fields': ('hero_image',),
        }),
        ('Informations générales', {
            'fields': ('name', 'slug', 'icon', 'tagline', 'description'),
        }),
        ('Apparence & Publication', {
            'fields': ('color_accent', 'order', 'is_active'),
        }),
    )

    def cover_thumb(self, obj):
        if obj.hero_image:
            return format_html(
                '<img src="{}" style="width:56px;height:40px;object-fit:cover;border-radius:6px;border:2px solid #C9A84C;">',
                obj.hero_image.url
            )
        return format_html(
            '<div style="width:56px;height:40px;background:#152438;border-radius:6px;display:flex;align-items:center;'
            'justify-content:center;font-size:1.2rem;border:1px dashed rgba(201,168,76,.4);">📷</div>'
        )
    cover_thumb.short_description = 'Image'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ['cover_thumb', 'title', 'domain', 'client', 'location', 'year', 'is_featured']
    list_display_links = ['cover_thumb', 'title']
    list_editable = ['is_featured']
    list_filter   = ['domain', 'is_featured', 'year']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'client', 'location']
    inlines       = [ProjectPhotoInline]

    fieldsets = (
        ('🖼️  Image principale', {
            'description': 'Image de couverture du projet (affichée en vignette dans le portfolio).',
            'fields': ('cover_image',),
        }),
        ('Informations projet', {
            'fields': ('domain', 'title', 'slug', 'description', 'client', 'location', 'year'),
        }),
        ('Publication', {
            'fields': ('is_featured',),
        }),
    )

    def cover_thumb(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="width:56px;height:40px;object-fit:cover;border-radius:6px;">',
                obj.cover_image.url
            )
        return '—'
    cover_thumb.short_description = 'Photo'


@admin.register(ProjectPhoto)
class ProjectPhotoAdmin(admin.ModelAdmin):
    list_display = ['thumb', 'project', 'caption', 'order']
    list_filter  = ['project']

    def thumb(self, obj):
        return format_html('<img src="{}" style="width:48px;height:34px;object-fit:cover;border-radius:4px;">', obj.image.url)
    thumb.short_description = '·'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display  = ['name', 'company', 'rating', 'domain', 'is_featured', 'created_at']
    list_editable = ['is_featured']
    list_filter   = ['domain', 'rating', 'is_featured']
    search_fields = ['name', 'company', 'content']


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display  = ['photo_thumb', 'name', 'role', 'order', 'is_active']
    list_display_links = ['photo_thumb', 'name']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'role']

    def photo_thumb(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:36px;height:36px;border-radius:50%;object-fit:cover;">', obj.photo.url)
        return '👤'
    photo_thumb.short_description = '·'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ['name', 'email', 'subject', 'domain', 'status', 'created_at']
    list_editable = ['status']
    list_filter   = ['status', 'domain', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'domain', 'created_at']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display  = ['question', 'domain', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter   = ['domain', 'is_active']
    search_fields = ['question', 'answer']


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display  = ['label', 'value', 'suffix', 'order']
    list_editable = ['order']

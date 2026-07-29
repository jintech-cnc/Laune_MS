from django.contrib import admin
from .models import DemandeDevis


@admin.register(DemandeDevis)
class DemandeDevisAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'domain', 'project_title', 'budget', 'urgency', 'status', 'created_at']
    list_editable = ['status']
    list_filter = ['status', 'domain', 'budget', 'urgency', 'created_at']
    search_fields = ['name', 'email', 'company', 'project_title', 'description']
    readonly_fields = ['name', 'email', 'phone', 'company', 'domain', 'project_title', 'description', 'location', 'budget', 'urgency', 'attachment', 'created_at']
    fieldsets = (
        ('Informations client', {'fields': ('name', 'email', 'phone', 'company')}),
        ('Projet', {'fields': ('domain', 'project_title', 'description', 'location', 'budget', 'urgency', 'attachment')}),
        ('Gestion', {'fields': ('status', 'admin_notes', 'created_at')}),
    )

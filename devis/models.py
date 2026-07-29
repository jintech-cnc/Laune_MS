from django.db import models
from core.models import ServiceDomain


class DemandeDevis(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('reviewing', 'En étude'),
        ('quoted', 'Devis envoyé'),
        ('accepted', 'Accepté'),
        ('rejected', 'Refusé'),
    ]
    BUDGET_CHOICES = [
        ('less_500k', 'Moins de 500 000 FCFA'),
        ('500k_2m', '500 000 — 2 000 000 FCFA'),
        ('2m_10m', '2 000 000 — 10 000 000 FCFA'),
        ('more_10m', 'Plus de 10 000 000 FCFA'),
        ('undefined', 'Budget à définir'),
    ]
    URGENCY_CHOICES = [
        ('asap', 'Urgent (moins de 2 semaines)'),
        ('month', 'Dans le mois'),
        ('quarter', 'Dans le trimestre'),
        ('flexible', 'Flexible'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=100, blank=True)
    domain = models.ForeignKey(ServiceDomain, on_delete=models.SET_NULL, null=True)
    project_title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    budget = models.CharField(max_length=20, choices=BUDGET_CHOICES, default='undefined')
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='flexible')
    attachment = models.FileField(upload_to='devis_attachments/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Demande de devis'
        verbose_name_plural = 'Demandes de devis'

    def __str__(self):
        return f"{self.name} — {self.project_title}"

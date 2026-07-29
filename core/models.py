from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class ServiceDomain(models.Model):
    ICONS = [
        ('architecture', 'Architecture'),
        ('computer', 'Informatique'),
        ('plumbing', 'Plomberie'),
        ('electrical', 'Électricité'),
        ('construction', 'Construction'),
        ('landscaping', 'Paysagisme'),
        ('cleaning', 'Nettoyage'),
        ('security', 'Sécurité'),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, choices=ICONS, default='construction')
    tagline = models.CharField(max_length=200)
    description = models.TextField()
    hero_image = models.ImageField(upload_to='services/', blank=True, null=True)
    color_accent = models.CharField(max_length=7, default='#C9A84C')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ServiceFeature(models.Model):
    domain = models.ForeignKey(ServiceDomain, on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon_svg = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.domain.name} — {self.title}"


class Project(models.Model):
    domain = models.ForeignKey(ServiceDomain, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    client = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=150, blank=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='projects/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProjectPhoto(models.Model):
    """Galerie multi-photos pour chaque projet"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Photo #{self.order} — {self.project.title}"


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=150, blank=True)
    company = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    domain = models.ForeignKey(ServiceDomain, on_delete=models.SET_NULL, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return f"{self.name} — {self.rating}★"


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=150)
    bio = models.TextField()
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} — {self.role}"


class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'Nouveau'),
        ('read', 'Lu'),
        ('replied', 'Répondu'),
        ('closed', 'Clôturé'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    domain = models.ForeignKey(ServiceDomain, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.subject}"


class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    domain = models.ForeignKey(ServiceDomain, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


class Statistic(models.Model):
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    suffix = models.CharField(max_length=20, blank=True)
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.value}{self.suffix} {self.label}"

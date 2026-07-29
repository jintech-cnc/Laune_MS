from django.contrib import admin
from .models import Article, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'domain', 'is_published', 'is_featured', 'views_count', 'published_at']
    list_editable = ['is_published', 'is_featured']
    list_filter = ['is_published', 'is_featured', 'category', 'domain', 'author']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'excerpt', 'content']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    fieldsets = (
        ('Contenu', {'fields': ('title', 'slug', 'excerpt', 'content', 'cover_image')}),
        ('Classification', {'fields': ('author', 'category', 'domain')}),
        ('Publication', {'fields': ('is_published', 'is_featured', 'published_at')}),
        ('Statistiques', {'fields': ('views_count', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('blog/', include('blog.urls')),
    path('devis/', include('devis.urls')),
    path('catalogue/', include('boutique.urls')),
    path('chat/', include('chat.urls')),
    path('auth/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "La Une Multiservice — Administration"
admin.site.site_title = "La Une Multiservice"
admin.site.index_title = "Tableau de bord"

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('ganado/', include('ganado.urls')),
    path('sanitario/', include('sanitario.urls')),
    path('alimentacion/', include('alimentacion.urls')),
    path('reportes/', include('reportes.urls')),
    path('qr/', include('qr.urls')),
    path('usuarios/', include('usuarios.urls')),
    # Logout directo (también funciona en /usuarios/logout/)
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

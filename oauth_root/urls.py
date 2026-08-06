from django.contrib import admin
from django.urls import path, include
from accounts.views import register, user_info, index, profile_page, AutoAuthorizationView, profile_edit
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/authorize/', AutoAuthorizationView.as_view(), name='authorize'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', register, name='register'),
    path('api/userinfo/', user_info, name='userinfo'),
    path('', index, name='index'),
    path('profile/', profile_page, name='profile_page'),
    path('profile/edit/', profile_edit, name='profile_edit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

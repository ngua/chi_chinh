"""chi_chinh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.utils import timezone
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.views.decorators.http import last_modified
from django.views.i18n import JavaScriptCatalog


LAST_MODIFIED = timezone.now()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('common.urls')),
    path('recipes/', include('recipes.urls')),
    path('contact/', include('contact.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('', include('common.urls')),
    path('recipes/', include('recipes.urls')),
    path('contact/', include('contact.urls')),
    path(
        'jsi18n/',
        last_modified(lambda req, **kw: LAST_MODIFIED)(
            JavaScriptCatalog.as_view(packages=['recipes']),
        ),
        name='js-catalog'
    ),
)

if os.environ.get('DJANGO_SETTINGS_MODULE') == 'settings.dev':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

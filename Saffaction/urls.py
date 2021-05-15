from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls, name='admin_index'),
    path('', include(('core.urls', 'core'), namespace='core')),
    path('healthcheck/', lambda r: HttpResponse())
]

if settings.DEBUG:
    pass
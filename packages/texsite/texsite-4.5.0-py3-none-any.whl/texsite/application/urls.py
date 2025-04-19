from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from texsite.core.views import server_error


handler500 = server_error


urlpatterns = [
    url(r'^django/', admin.site.urls),
    url(r'^wagtail/', include('wagtail.admin.urls')),
    url(r'^documents/', include('wagtail.documents.urls')),
    url(r'', include('wagtail.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

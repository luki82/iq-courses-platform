from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from core.sitemaps import sitemaps
from core.views import robots_txt

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("iq-test/", include("iqtest.urls")),
    path("courses/", include("courses.urls")),
    path("ielts/", include("ielts.urls")),
    path("billing/", include("billing.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

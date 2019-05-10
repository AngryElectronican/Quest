from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from .import views
urlpatterns = [
    url(r'^request', views.request),
    url(r'^interface', views.interface),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
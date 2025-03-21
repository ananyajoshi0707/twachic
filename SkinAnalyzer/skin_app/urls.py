from django.urls import path
from .views import upload_image
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("", upload_image, name="upload_image"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
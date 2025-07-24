from django.contrib import admin
from django.urls import path, include
app_label = "skin_app"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("skin_app.urls")),
]


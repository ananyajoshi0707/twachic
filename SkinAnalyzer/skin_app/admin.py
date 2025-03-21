from django.contrib import admin
from .models import SkinAnalysis

class SkinAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'recommendations', 'uploaded_at')

admin.site.register(SkinAnalysis,SkinAnalysisAdmin)


# Register your models here.

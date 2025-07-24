from django.contrib import admin 
from .models import SkinAnalysis

@admin.register(SkinAnalysis)
class SkinAnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_preview', 'condition_short', 'recommendations', 'uploaded_at')
    readonly_fields = ('image_preview',)
    search_fields = ('condition', 'recommendations')
    list_filter = ('uploaded_at',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" />'
        return "No Image"
    image_preview.allow_tags = True
    image_preview.short_description = "Image"

    def condition_short(self, obj):
        return obj.condition[:50] if obj.condition else "Pending"
    condition_short.short_description = "Condition"

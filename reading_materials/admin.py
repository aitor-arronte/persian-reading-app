from django.contrib import admin
from .models import *
from tinymce.widgets import TinyMCE
from django.db import models



class ReadingAdmin(admin.ModelAdmin):
    class Meta:
        model = ReadingMaterial
        exclude = []
    list_display = ('title', )
    list_filter = ('title',)
    fields = ('title', 'instructions', 'text','audio', 'difficulty', 'video', 'image', 'pdf', 'quizzes', 'order')

    formfield_overrides = {

        models.TextField: {'widget': TinyMCE()}

    }

    search_fields = ('title', )



class UserProgress(admin.ModelAdmin):
    filter_horizontal = ('passed_materials',)

admin.site.register(ReadingMaterial, ReadingAdmin)
admin.site.register(Profile)
admin.site.register(Progress, UserProgress)
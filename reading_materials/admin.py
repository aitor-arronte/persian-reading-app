from django.contrib import admin
from .models import *
from tinymce.widgets import TinyMCE
from django.db import models
'''
class TextMedia:
    js = [
         '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
        '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]
'''


class GlossInline(admin.TabularInline):
    model = ReadingText
    extra=1
    formfield_overrides = {

        models.TextField: {'widget': TinyMCE()}

    }


class AnswerInline(admin.TabularInline):
    model = Answer
    extra=2
    formfield_overrides = {

        models.TextField: {'widget': TinyMCE()}

    }



class ReadingAdmin(admin.ModelAdmin):
    class Meta:
        model = ReadingMaterial
        exclude = []
    list_display = ('title', )
    list_filter = ('title',)
    fields = ('title', 'rubric', 'audio', 'difficulty', 'video', 'image', 'quiz_type', 'quiz_instructions'
              ,'order', 'use_glossing')

    formfield_overrides = {

        models.TextField: {'widget': TinyMCE()}

    }

    search_fields = ('title', )
    inlines = [AnswerInline, GlossInline]




admin.site.register(Answer)
admin.site.register(Response)
admin.site.register(ReadingMaterial, ReadingAdmin)
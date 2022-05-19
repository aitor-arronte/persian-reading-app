from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from reading_app import settings
from reading_materials.views import *

urlpatterns = [
		path('accounts/', include(('django.contrib.auth.urls','django.contrib.auth'), namespace='auth'), name="signin"),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
		path('material/<str:level>/<int:material_id>', show_material),
		path('tinymce/[id]',include('tinymce.urls')),
    path('', TemplateView.as_view(template_name='reading_materials/home.html'), name='home'),
		path('proficiency/', proficiency_levels),
		path('reading/', TemplateView.as_view(template_name='reading_materials/reading_material-2.html')),
		path('profile/', get_profile),
		path('save_responses', save_responses, name='save_responses'),
		path('create_entries', create_entries)
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
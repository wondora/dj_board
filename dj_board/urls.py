from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView # Import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', include('freeboard.urls')), # 루트 URL을 freeboard 앱으로 연결
    path('accounts/', include('django.contrib.auth.urls')), # Django 내장 인증 URL 추가
]


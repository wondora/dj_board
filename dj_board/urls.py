from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView # Import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('board/', include('freeboard.urls')), # 게시판 URL을 /board/ 아래로 이동
    path('', TemplateView.as_view(template_name='freeboard/index.html'), name='home'), # 루트 URL을 index.html로 연결
    path('accounts/', include('django.contrib.auth.urls')), # Django 내장 인증 URL 추가
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
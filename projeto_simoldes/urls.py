"""
URL configuration for projeto_simoldes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from webapp import views 
from webapp.views import listar_modelos_step, pagina_principal, login, checklist

urlpatterns = [
    path('modelos', listar_modelos_step, name='listar_modelos_step'),
    path('', login, name ='login'),
    # path('pagina_principal', pagina_principal, name='pagina_principal'),
    path('checklist', checklist, name='checklist'),
    path('pagina_principal', views.pagina_principal, name='pagina_principal'),
    path('atualizar/', views.atualizar_status, name='atualizar_status'),
    path('atualizar_checklist/', views.atualizar_status_checklist, name='atualizar_status_checklist'),
    path('pagina/<str:nome_aba>/', views.pagina_principal, name='listar_arquivos_com_aba'),
    path('checklist/<str:nome_aba>/', views.checklist, name='listar_arquivos_checklist')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)# Vê se a pasta MEDIA existe

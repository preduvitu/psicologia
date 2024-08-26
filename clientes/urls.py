from django.urls import path
from django.conf import settings  
from django.conf.urls.static import static 
from . import views
from .views import show_file, show_file2

app_name = 'clientes'

urlpatterns = [
    path('registro/', views.cliente_cadastro, name='cliente_cadastro'),
    path('atualizar/', views.cliente_atualizar, name='cliente_atualizar'),
    path('detalhe/<int:pk>/', views.detalhes, name='detalhes'),
    path('consultas/', views.consulta_lista, name='consulta_list'),
    path('consultas/criar/', views.consulta_cadastro, name='consulta_create'),
    path('consultas/editar/<int:pk>/', views.consulta_atualizar, name='consulta_update'),
    path('consultas/excluir/<int:pk>/', views.consulta_excluir, name='consulta_delete'),
    path('media/', show_file, name='show_file'),
    path('painel/', views.painel, name="show_file2"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.MEDIA_URL_PRONTUARIOS, document_root=settings.MEDIA_ROOT_PRONTUARIOS)
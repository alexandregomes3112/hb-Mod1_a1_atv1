"""
URL configuration for reservas app
"""
from django.urls import path
from . import views

urlpatterns = [
    # Públicas
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),

    # Autenticadas
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reservar/', views.criar_reserva, name='criar_reserva'),
    path('minhas-reservas/', views.minhas_reservas, name='minhas_reservas'),
    path('reserva/<int:reserva_id>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),
    path('salas/', views.listar_salas, name='listar_salas'),

    # Admin
    path('admin/', views.painel_admin, name='painel_admin'),
    path('admin/reservas/', views.todas_reservas, name='todas_reservas'),
    path('admin/reserva/<int:reserva_id>/cancelar/', views.cancelar_reserva_admin, name='cancelar_reserva_admin'),
    path('admin/salas/', views.gerenciar_salas, name='gerenciar_salas'),
    path('admin/sala/criar/', views.criar_sala, name='criar_sala'),
    path('admin/sala/<int:sala_id>/editar/', views.editar_sala, name='editar_sala'),
    path('admin/sala/<int:sala_id>/deletar/', views.deletar_sala, name='deletar_sala'),
    path('admin/relatorio/', views.relatorio_uso, name='relatorio_uso'),
]

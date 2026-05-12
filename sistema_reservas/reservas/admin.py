from django.contrib import admin
from .models import Sala, Reserva, Auditoria, PerfilUsuario


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'capacidade', 'localizacao', 'ativa', 'data_criacao')
    list_filter = ('ativa', 'data_criacao')
    search_fields = ('nome', 'localizacao')
    readonly_fields = ('data_criacao', 'data_atualizacao')


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'sala', 'data_reserva', 'hora_inicio', 'hora_fim', 'status')
    list_filter = ('status', 'data_reserva', 'sala')
    search_fields = ('usuario__username', 'sala__nome', 'motivo')
    readonly_fields = ('data_criacao', 'data_cancelamento')
    fieldsets = (
        ('Informações Básicas', {'fields': ('usuario', 'sala', 'motivo', 'status')}),
        ('Horário', {'fields': ('data_reserva', 'hora_inicio', 'hora_fim')}),
        ('Cancelamento', {'fields': ('data_cancelamento', 'motivo_cancelamento')}),
        ('Auditoria', {'fields': ('data_criacao',), 'classes': ('collapse',)}),
    )


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_acao', 'data_acao', 'ip_address')
    list_filter = ('tipo_acao', 'data_acao')
    search_fields = ('usuario__username', 'descricao')
    readonly_fields = ('usuario', 'tipo_acao', 'descricao', 'data_acao', 'ip_address')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'ativo', 'data_criacao')
    list_filter = ('tipo', 'ativo', 'data_criacao')
    search_fields = ('usuario__username', 'usuario__email')

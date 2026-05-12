from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Sala(models.Model):
    """Modelo de Sala disponível para reserva"""
    nome = models.CharField(max_length=100, unique=True)
    capacidade = models.IntegerField()
    localizacao = models.CharField(max_length=150)
    recursos = models.TextField(help_text="Ex: Projetor, Quadro, Whiteboard, TV")
    ativa = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'

    def __str__(self):
        return self.nome


class Reserva(models.Model):
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('cancelada', 'Cancelada'),
        ('concluida', 'Concluída'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='reservas')
    data_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    motivo = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativa')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_cancelamento = models.DateTimeField(null=True, blank=True)
    motivo_cancelamento = models.TextField(blank=True)

    class Meta:
        ordering = ['-data_reserva', '-hora_inicio']
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        unique_together = ('sala', 'data_reserva', 'hora_inicio')

    def __str__(self):
        return f"{self.sala.nome} - {self.data_reserva} às {self.hora_inicio}"

    def clean(self):
        """Validações customizadas"""
        # Verificar se a hora de fim é após a hora de início
        if self.hora_fim <= self.hora_inicio:
            raise ValidationError("Hora de fim deve ser posterior à hora de início")

        # Verificar duração mínima (15 minutos)
        from datetime import datetime, timedelta
        start = datetime.combine(self.data_reserva, self.hora_inicio)
        end = datetime.combine(self.data_reserva, self.hora_fim)
        duracao = (end - start).total_seconds() / 60
        if duracao < 15:
            raise ValidationError("Duração mínima da reserva é 15 minutos")

        # Verificar se a data não é no passado
        if self.data_reserva < timezone.now().date():
            raise ValidationError("Não é possível fazer reserva para datas passadas")

        # Verificar conflitos com outras reservas
        conflitos = Reserva.objects.filter(
            sala=self.sala,
            data_reserva=self.data_reserva,
            status='ativa'
        ).exclude(id=self.id).filter(
            models.Q(hora_inicio__lt=self.hora_fim) & models.Q(hora_fim__gt=self.hora_inicio)
        )

        if conflitos.exists():
            raise ValidationError(f"Conflito de horário! Reservas existentes: {', '.join([str(r) for r in conflitos])}")

    def pode_cancelar(self, usuario):
        """Verifica se o usuário pode cancelar esta reserva"""
        # Admin pode cancelar qualquer reserva
        if usuario.is_staff:
            return True, None

        # Usuário comum só pode cancelar suas próprias reservas
        if usuario != self.usuario:
            return False, "Você não tem permissão para cancelar esta reserva"

        # Verificar antecedência mínima (2 horas para usuário comum)
        from datetime import datetime, timedelta
        agora = timezone.now()
        horario_reserva = datetime.combine(self.data_reserva, self.hora_inicio)
        horario_reserva = timezone.make_aware(horario_reserva) if timezone.is_naive(horario_reserva) else horario_reserva

        tempo_restante = (horario_reserva - agora).total_seconds() / 3600
        if tempo_restante < 2:
            return False, "Cancelamento deve ser feito com mínimo 2 horas de antecedência"

        return True, None

    def cancelar(self, motivo=""):
        """Cancela a reserva"""
        self.status = 'cancelada'
        self.data_cancelamento = timezone.now()
        self.motivo_cancelamento = motivo
        self.save()


class Auditoria(models.Model):
    TIPO_ACAO = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('criacao_reserva', 'Criação de Reserva'),
        ('cancelamento_reserva', 'Cancelamento de Reserva'),
        ('criacao_sala', 'Criação de Sala'),
        ('edicao_sala', 'Edição de Sala'),
        ('deletar_sala', 'Deleção de Sala'),
        ('acesso_admin', 'Acesso ao Admin'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auditorias')
    tipo_acao = models.CharField(max_length=50, choices=TIPO_ACAO)
    descricao = models.TextField()
    data_acao = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-data_acao']
        verbose_name = 'Auditoria'
        verbose_name_plural = 'Auditorias'

    def __str__(self):
        return f"{self.usuario.username} - {self.tipo_acao} em {self.data_acao}"


class PerfilUsuario(models.Model):
    """Perfil adicional do usuário para gerenciar permissões"""
    TIPO_USUARIO = [
        ('comum', 'Usuário Comum'),
        ('admin', 'Administrador'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO, default='comum')
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'

    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_display()}"

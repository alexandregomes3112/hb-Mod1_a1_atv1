from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta
import logging

from .models import Reserva, Sala, Auditoria, PerfilUsuario
from .forms import (
    RegistroForm, LoginForm, ReservaForm, SalaForm,
    CancelamentoReservaForm, FiltroReservasForm
)

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """Obtém o IP do cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def registrar_auditoria(usuario, tipo_acao, descricao, request=None):
    """Registra ações em auditoria"""
    Auditoria.objects.create(
        usuario=usuario,
        tipo_acao=tipo_acao,
        descricao=descricao,
        ip_address=get_client_ip(request) if request else None
    )


def enviar_email_confirmacao(usuario, reserva, tipo='confirmacao'):
    """Envia email de confirmação/cancelamento (para desenvolvimento, exibe no console)"""
    if tipo == 'confirmacao':
        subject = f"Reserva Confirmada - {reserva.sala.nome}"
        message = f"""
Olá {usuario.first_name},

Sua reserva foi confirmada com sucesso!

Detalhes:
- Sala: {reserva.sala.nome}
- Data: {reserva.data_reserva.strftime('%d/%m/%Y')}
- Horário: {reserva.hora_inicio.strftime('%H:%M')} até {reserva.hora_fim.strftime('%H:%M')}
- Motivo: {reserva.motivo}

ID da Reserva: {reserva.id}

Atenciosamente,
Sistema de Reserva de Salas
        """
    else:
        subject = f"Reserva Cancelada - {reserva.sala.nome}"
        message = f"""
Olá {usuario.first_name},

Sua reserva foi cancelada.

Detalhes:
- Sala: {reserva.sala.nome}
- Data: {reserva.data_reserva.strftime('%d/%m/%Y')}
- Horário: {reserva.hora_inicio.strftime('%H:%M')} até {reserva.hora_fim.strftime('%H:%M')}
- Motivo do Cancelamento: {reserva.motivo_cancelamento or 'Não especificado'}

ID da Reserva: {reserva.id}

Atenciosamente,
Sistema de Reserva de Salas
        """

    try:
        send_mail(
            subject,
            message,
            'noreply@sistemareservas.local',
            [usuario.email],
            fail_silently=False,
        )
        logger.info(f"Email {tipo} enviado para {usuario.email}")
    except Exception as e:
        logger.error(f"Erro ao enviar email: {str(e)}")


def is_admin(user):
    """Verifica se o usuário é admin"""
    return user.is_staff or user.is_superuser


# ============ Views Públicas ============

def index(request):
    """Página inicial"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def login_view(request):
    """View de login"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                registrar_auditoria(user, 'login', 'Login realizado', request)
                messages.success(request, f'Bem-vindo, {user.first_name}!')
                return redirect('dashboard')
    else:
        form = LoginForm()

    return render(request, 'reservas/login.html', {'form': form})


def logout_view(request):
    """View de logout"""
    if request.user.is_authenticated:
        registrar_auditoria(request.user, 'logout', 'Logout realizado', request)
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso!')
    return redirect('login')


def registro_view(request):
    """View de registro de novo usuário"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Criar perfil padrão como usuário comum
            PerfilUsuario.objects.create(user=user, tipo='comum')
            login(request, user)
            registrar_auditoria(user, 'login', 'Novo usuário registrado e logado', request)
            messages.success(request, 'Registro realizado com sucesso! Bem-vindo!')
            return redirect('dashboard')
    else:
        form = RegistroForm()

    return render(request, 'reservas/registro.html', {'form': form})


# ============ Views Autenticadas ============

@login_required(login_url='login')
def dashboard(request):
    """Dashboard principal"""
    usuario = request.user
    proximas_reservas = usuario.reservas.filter(
        status='ativa',
        data_reserva__gte=timezone.now().date()
    ).order_by('data_reserva', 'hora_inicio')[:5]

    context = {
        'proximas_reservas': proximas_reservas,
        'total_reservas': usuario.reservas.filter(status='ativa').count(),
        'salas_disponiveis': Sala.objects.filter(ativa=True).count(),
    }
    return render(request, 'reservas/dashboard.html', context)


@login_required(login_url='login')
def criar_reserva(request):
    """View para criar nova reserva"""
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            try:
                reserva = form.save(commit=False)
                reserva.usuario = request.user
                reserva.full_clean()  # Validações do model
                reserva.save()

                registrar_auditoria(
                    request.user,
                    'criacao_reserva',
                    f'Reserva criada: {reserva.sala.nome} - {reserva.data_reserva} às {reserva.hora_inicio}',
                    request
                )
                enviar_email_confirmacao(request.user, reserva, tipo='confirmacao')
                messages.success(request, 'Reserva criada com sucesso! Email de confirmação enviado.')
                return redirect('minhas_reservas')

            except Exception as e:
                messages.error(request, f'Erro ao criar reserva: {str(e)}')
    else:
        form = ReservaForm()

    # Obter disponibilidade das salas se requisição AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        sala_id = request.GET.get('sala_id')
        data = request.GET.get('data')
        if sala_id and data:
            return JsonResponse(get_salas_disponiveis(sala_id, data), safe=False)

    salas = Sala.objects.filter(ativa=True)
    context = {'form': form, 'salas': salas}
    return render(request, 'reservas/criar_reserva.html', context)


def get_salas_disponiveis(sala_id, data_str):
    """Obtém salas disponíveis para uma data específica (AJAX)"""
    try:
        data = datetime.strptime(data_str, '%Y-%m-%d').date()
        salas_disponiveis = []

        for sala in Sala.objects.filter(ativa=True):
            conflitos = Reserva.objects.filter(
                sala=sala,
                data_reserva=data,
                status='ativa'
            ).count()
            salas_disponiveis.append({
                'id': sala.id,
                'nome': sala.nome,
                'capacidade': sala.capacidade,
                'recursos': sala.recursos,
                'tem_conflitos': conflitos > 0,
                'conflitos': conflitos,
            })

        return salas_disponiveis
    except:
        return []


@login_required(login_url='login')
def minhas_reservas(request):
    """Listagem de minhas reservas"""
    usuario = request.user
    reservas = usuario.reservas.all()

    # Filtros
    form = FiltroReservasForm(request.GET)
    if form.is_valid():
        if form.cleaned_data.get('sala'):
            reservas = reservas.filter(sala=form.cleaned_data['sala'])
        if form.cleaned_data.get('data'):
            reservas = reservas.filter(data_reserva=form.cleaned_data['data'])
        if form.cleaned_data.get('status'):
            reservas = reservas.filter(status=form.cleaned_data['status'])

    context = {
        'reservas': reservas,
        'form': form,
    }
    return render(request, 'reservas/minhas_reservas.html', context)


@login_required(login_url='login')
def cancelar_reserva(request, reserva_id):
    """View para cancelar uma reserva"""
    reserva = get_object_or_404(Reserva, id=reserva_id)

    # Verificar permissões
    pode_cancelar, mensagem = reserva.pode_cancelar(request.user)
    if not pode_cancelar:
        messages.error(request, mensagem)
        return redirect('minhas_reservas')

    if request.method == 'POST':
        form = CancelamentoReservaForm(request.POST)
        if form.is_valid():
            motivo = form.cleaned_data.get('motivo_cancelamento', '')
            reserva.cancelar(motivo)
            registrar_auditoria(
                request.user,
                'cancelamento_reserva',
                f'Reserva cancelada: {reserva.sala.nome} - {reserva.data_reserva} às {reserva.hora_inicio}',
                request
            )
            enviar_email_confirmacao(request.user, reserva, tipo='cancelamento')
            messages.success(request, 'Reserva cancelada com sucesso!')
            return redirect('minhas_reservas')
    else:
        form = CancelamentoReservaForm()

    context = {'reserva': reserva, 'form': form}
    return render(request, 'reservas/cancelar_reserva.html', context)


@login_required(login_url='login')
def listar_salas(request):
    """Listagem de salas disponíveis"""
    salas = Sala.objects.filter(ativa=True).prefetch_related('reservas')

    # Contar reservas por sala
    salas_com_count = []
    for sala in salas:
        reservas_hoje = sala.reservas.filter(
            data_reserva=timezone.now().date(),
            status='ativa'
        ).count()
        salas_com_count.append({
            'sala': sala,
            'reservas_hoje': reservas_hoje,
        })

    context = {'salas': salas_com_count}
    return render(request, 'reservas/listar_salas.html', context)


# ============ Views Admin ============

def admin_required(function):
    """Decorator para verificar se o usuário é admin"""
    def wrap(request, *args, **kwargs):
        if not is_admin(request.user):
            messages.error(request, 'Acesso negado. Apenas administradores.')
            return redirect('dashboard')
        return function(request, *args, **kwargs)
    return wrap


@login_required(login_url='login')
@admin_required
def painel_admin(request):
    """Painel administrativo"""
    total_usuarios = User.objects.count()
    total_salas = Sala.objects.count()
    total_reservas = Reserva.objects.count()
    reservas_ativas = Reserva.objects.filter(status='ativa').count()

    reservas_proximas = Reserva.objects.filter(
        status='ativa',
        data_reserva__gte=timezone.now().date()
    ).order_by('data_reserva', 'hora_inicio')[:10]

    context = {
        'total_usuarios': total_usuarios,
        'total_salas': total_salas,
        'total_reservas': total_reservas,
        'reservas_ativas': reservas_ativas,
        'reservas_proximas': reservas_proximas,
    }
    return render(request, 'reservas/admin/painel_admin.html', context)


@login_required(login_url='login')
@admin_required
def todas_reservas(request):
    """Admin: Listagem de todas as reservas"""
    reservas = Reserva.objects.select_related('usuario', 'sala')

    form = FiltroReservasForm(request.GET)
    if form.is_valid():
        if form.cleaned_data.get('sala'):
            reservas = reservas.filter(sala=form.cleaned_data['sala'])
        if form.cleaned_data.get('data'):
            reservas = reservas.filter(data_reserva=form.cleaned_data['data'])
        if form.cleaned_data.get('status'):
            reservas = reservas.filter(status=form.cleaned_data['status'])

    context = {
        'reservas': reservas,
        'form': form,
    }
    return render(request, 'reservas/admin/todas_reservas.html', context)


@login_required(login_url='login')
@admin_required
def cancelar_reserva_admin(request, reserva_id):
    """Admin: Cancelar qualquer reserva"""
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if request.method == 'POST':
        motivo = request.POST.get('motivo_cancelamento', '')
        reserva.cancelar(motivo)
        registrar_auditoria(
            request.user,
            'cancelamento_reserva',
            f'Admin cancelou reserva de {reserva.usuario.username}: {reserva.sala.nome}',
            request
        )
        enviar_email_confirmacao(reserva.usuario, reserva, tipo='cancelamento')
        messages.success(request, f'Reserva de {reserva.usuario.first_name} cancelada!')
        return redirect('todas_reservas')

    context = {'reserva': reserva}
    return render(request, 'reservas/admin/cancelar_reserva_admin.html', context)


@login_required(login_url='login')
@admin_required
def gerenciar_salas(request):
    """Admin: Gerenciar salas"""
    salas = Sala.objects.all()
    context = {'salas': salas}
    return render(request, 'reservas/admin/gerenciar_salas.html', context)


@login_required(login_url='login')
@admin_required
def criar_sala(request):
    """Admin: Criar nova sala"""
    if request.method == 'POST':
        form = SalaForm(request.POST)
        if form.is_valid():
            sala = form.save()
            registrar_auditoria(
                request.user,
                'criacao_sala',
                f'Sala criada: {sala.nome}',
                request
            )
            messages.success(request, f'Sala "{sala.nome}" criada com sucesso!')
            return redirect('gerenciar_salas')
    else:
        form = SalaForm()

    context = {'form': form, 'titulo': 'Criar Nova Sala'}
    return render(request, 'reservas/admin/sala_form.html', context)


@login_required(login_url='login')
@admin_required
def editar_sala(request, sala_id):
    """Admin: Editar sala"""
    sala = get_object_or_404(Sala, id=sala_id)

    if request.method == 'POST':
        form = SalaForm(request.POST, instance=sala)
        if form.is_valid():
            form.save()
            registrar_auditoria(
                request.user,
                'edicao_sala',
                f'Sala editada: {sala.nome}',
                request
            )
            messages.success(request, 'Sala atualizada com sucesso!')
            return redirect('gerenciar_salas')
    else:
        form = SalaForm(instance=sala)

    context = {'form': form, 'sala': sala, 'titulo': f'Editar Sala: {sala.nome}'}
    return render(request, 'reservas/admin/sala_form.html', context)


@login_required(login_url='login')
@admin_required
def deletar_sala(request, sala_id):
    """Admin: Deletar sala"""
    sala = get_object_or_404(Sala, id=sala_id)

    if request.method == 'POST':
        nome_sala = sala.nome
        sala.delete()
        registrar_auditoria(
            request.user,
            'deletar_sala',
            f'Sala deletada: {nome_sala}',
            request
        )
        messages.success(request, 'Sala deletada com sucesso!')
        return redirect('gerenciar_salas')

    context = {'sala': sala}
    return render(request, 'reservas/admin/deletar_sala.html', context)


@login_required(login_url='login')
@admin_required
def relatorio_uso(request):
    """Admin: Relatório de uso das salas"""
    salas = Sala.objects.all()
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    relatorio = []
    for sala in salas:
        reservas = sala.reservas.filter(status__in=['ativa', 'concluida'])

        if data_inicio:
            reservas = reservas.filter(data_reserva__gte=data_inicio)
        if data_fim:
            reservas = reservas.filter(data_reserva__lte=data_fim)

        total_reservas = reservas.count()
        hora_total = sum([
            (datetime.combine(r.data_reserva, r.hora_fim) -
             datetime.combine(r.data_reserva, r.hora_inicio)).total_seconds() / 3600
            for r in reservas
        ], 0)

        relatorio.append({
            'sala': sala,
            'total_reservas': total_reservas,
            'horas_total': round(hora_total, 2),
            'taxa_ocupacao': f"{(total_reservas / max(1, 30)) * 100:.1f}%",
        })

    context = {
        'relatorio': relatorio,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    return render(request, 'reservas/admin/relatorio_uso.html', context)

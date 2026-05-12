from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Reserva, Sala
from django.utils import timezone


class RegistroForm(UserCreationForm):
    """Formulário para registro de novo usuário"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome Completo'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password1', 'password2')
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Senha'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar Senha'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está cadastrado")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Formulário customizado de login"""
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
        label='Senha'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remover o label padrão
        self.fields['username'].label = 'Email'


class ReservaForm(forms.ModelForm):
    """Formulário para criar/editar reserva"""
    sala = forms.ModelChoiceField(
        queryset=Sala.objects.filter(ativa=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Sala'
    )
    data_reserva = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Data da Reserva'
    )
    hora_inicio = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        label='Hora de Início'
    )
    hora_fim = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        label='Hora de Término'
    )
    motivo = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motivo da reunião'}),
        label='Motivo da Reunião'
    )

    class Meta:
        model = Reserva
        fields = ('sala', 'data_reserva', 'hora_inicio', 'hora_fim', 'motivo')

    def clean(self):
        cleaned_data = super().clean()
        data_reserva = cleaned_data.get('data_reserva')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fim = cleaned_data.get('hora_fim')

        if data_reserva and data_reserva < timezone.now().date():
            raise forms.ValidationError("Não é possível fazer reserva para datas passadas")

        if hora_inicio and hora_fim and hora_fim <= hora_inicio:
            raise forms.ValidationError("Hora de término deve ser posterior à hora de início")

        if hora_inicio and hora_fim:
            from datetime import datetime
            start = datetime.combine(data_reserva or timezone.now().date(), hora_inicio)
            end = datetime.combine(data_reserva or timezone.now().date(), hora_fim)
            duracao = (end - start).total_seconds() / 60
            if duracao < 15:
                raise forms.ValidationError("Duração mínima da reserva é 15 minutos")

        return cleaned_data


class SalaForm(forms.ModelForm):
    """Formulário para criar/editar sala (apenas admin)"""
    nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Sala'})
    )
    capacidade = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacidade'}),
        min_value=1
    )
    localizacao = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Localização'})
    )
    recursos = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ex: Projetor, Quadro, Whiteboard, TV'}),
        label='Recursos Disponíveis'
    )
    ativa = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Ativa',
        initial=True
    )

    class Meta:
        model = Sala
        fields = ('nome', 'capacidade', 'localizacao', 'recursos', 'ativa')


class CancelamentoReservaForm(forms.Form):
    """Formulário para cancelar reserva"""
    motivo_cancelamento = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Motivo do cancelamento (opcional)'
        }),
        label='Motivo do Cancelamento'
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class FiltroReservasForm(forms.Form):
    """Formulário para filtrar reservas"""
    sala = forms.ModelChoiceField(
        queryset=Sala.objects.filter(ativa=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Sala'
    )
    data = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Data'
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', '---')] + Reserva.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Status'
    )

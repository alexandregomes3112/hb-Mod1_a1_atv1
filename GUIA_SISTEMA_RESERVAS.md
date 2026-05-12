# 🏢 Sistema de Reserva de Salas - Django

Sistema completo de reserva de salas desenvolvido com Django e SQLite, baseado na estrutura SDLC proposta na atividade prática.

## ✨ Funcionalidades Principais

### Usuários Comuns
- ✅ Registro e autenticação
- ✅ Fazer reservas de salas
- ✅ Listar suas reservas
- ✅ Cancelar reservas (com 2 horas de antecedência)
- ✅ Visualizar salas disponíveis

### Administradores
- ✅ Todas as funcionalidades de usuário comum
- ✅ Gerenciar salas (criar, editar, deletar)
- ✅ Visualizar todas as reservas do sistema
- ✅ Cancelar qualquer reserva
- ✅ Gerar relatórios de uso das salas
- ✅ Painel administrativo

### Sistema
- ✅ Autenticação segura (Django ORM)
- ✅ Validação de conflitos de horários
- ✅ Duração mínima de 15 minutos por reserva
- ✅ Notificações por email (simuladas no console)
- ✅ Sistema de auditoria
- ✅ Responsivo e intuitivo

---

## 🚀 Instalação Rápida

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### Passo 1: Clonar/Acessar o Projeto
```bash
cd /ativ1
```

### Passo 2: Executar Script de Setup
```bash
chmod +x setup.sh
./setup.sh
```

O script irá:
1. Criar um ambiente virtual
2. Instalar dependências
3. Configurar o banco de dados
4. Criar um superusuário (admin)
5. Carregar dados de exemplo

### Passo 3: Iniciar o Servidor
```bash
cd sistema_reservas
python manage.py runserver
```

### Passo 4: Acessar a Aplicação
- **Sistema de Reservas**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin
- **Login**: Use o email e senha do superusuário criado

---

## 📁 Estrutura do Projeto

```
sistema_reservas/
├── config/                         # Configurações do Django
│   ├── settings.py                 # Configurações gerais
│   ├── urls.py                     # URLs raiz do projeto
│   ├── wsgi.py                     # WSGI para produção
│   └── asgi.py                     # ASGI para produção
│
├── reservas/                       # App principal
│   ├── models.py                   # Modelos (Sala, Reserva, Auditoria, etc)
│   ├── views.py                    # Lógica das views
│   ├── forms.py                    # Formulários
│   ├── urls.py                     # URLs da app
│   ├── admin.py                    # Configuração do Django Admin
│   ├── apps.py                     # Configuração da app
│   │
│   ├── templates/reservas/         # Templates HTML
│   │   ├── base.html               # Template base
│   │   ├── login.html              # Login
│   │   ├── registro.html           # Registro
│   │   ├── dashboard.html          # Dashboard
│   │   ├── criar_reserva.html      # Criar reserva
│   │   ├── minhas_reservas.html    # Listar minhas reservas
│   │   ├── cancelar_reserva.html   # Cancelar reserva
│   │   ├── listar_salas.html       # Listar salas
│   │   │
│   │   └── admin/                  # Templates admin
│   │       ├── painel_admin.html
│   │       ├── todas_reservas.html
│   │       ├── gerenciar_salas.html
│   │       ├── sala_form.html
│   │       └── relatorio_uso.html
│   │
│   └── migrations/                 # Migrações do banco (auto-criadas)
│
├── static/css/                     # Estilos CSS
│   └── style.css                   # Stylesheet completo
│
├── manage.py                       # Script de gerenciamento Django
├── db.sqlite3                      # Banco de dados SQLite
└── requirements.txt                # Dependências do projeto
```

---

## 🔑 Modelos de Dados

### Usuário (Django User padrão)
- Email, Senha, Nome, Data de Criação
- PerfilUsuario: Tipo (comum/admin), Ativo

### Sala
- Nome, Capacidade, Localização, Recursos
- Ativa (Boolean), Data de Criação/Atualização

### Reserva
- Usuário (FK), Sala (FK)
- Data, Hora Início, Hora Fim
- Motivo, Status (ativa/cancelada/concluída)
- Data de Cancelamento, Motivo de Cancelamento

### Auditoria
- Usuário (FK), Tipo de Ação
- Descrição, Data/Hora, IP Address

---

## 🔐 Segurança

- ✅ Senhas com hash (bcrypt via Django)
- ✅ Proteção CSRF em formulários
- ✅ Validação de entrada no backend
- ✅ Controle de acesso baseado em permissões
- ✅ Sistema de auditoria
- ✅ Prepared statements (ORM Django)

---

## 📝 Fluxos Principais

### 1. Criar Reserva
```
Login → Dashboard → Fazer Reserva → Preencher formulário → Validações → Salvar → Email
```

**Validações:**
- Data não pode ser no passado
- Duração mínima: 15 minutos
- Horário final > horário inicial
- Sem conflitos com outras reservas

### 2. Cancelar Reserva (Usuário Comum)
```
Minhas Reservas → Selecionar Reserva → Cancelar → Confirmar → Email
```

**Restrições:**
- Apenas suas próprias reservas
- Mínimo 2 horas de antecedência
- Admin pode cancelar qualquer reserva sem restrição

### 3. Gerenciar Salas (Admin)
```
Admin → Gerenciar Salas → CRUD de Salas
```

---

## 🧪 Testes

Para testar o sistema:

### 1. Criar conta comum
```
Clique em "Criar conta" → Preencha dados → Confirme
```

### 2. Criar conta admin (via setup)
```
Durante o setup, crie um superusuário
```

### 3. Testar fluxos
- Fazer reserva simples
- Tentar conflito de horário (deve ser rejeitado)
- Cancelar reserva
- Como admin, cancelar reserva de outro usuário
- Criar/editar/deletar salas

---

## 📊 Relatórios

### Painel Admin
Acesso via: Admin > Painel Administrativo

**Informações:**
- Total de usuários
- Total de salas
- Total de reservas
- Reservas ativas
- Próximas reservas

### Relatório de Uso
Acesso via: Admin > Relatório de Uso

**Dados por sala:**
- Total de reservas
- Horas totais reservadas
- Taxa de ocupação
- Período customizável

---

## 🐛 Troubleshooting

### Erro: "Módulo reservas não encontrado"
```bash
# Certifique-se que está na pasta correta
cd sistema_reservas

# Reexecute as migrações
python manage.py migrate
```

### Erro: "Static files not found"
```bash
# Recolha os arquivos estáticos
python manage.py collectstatic --noinput
```

### Erro de permissão ao rodar setup.sh
```bash
# Torne o arquivo executável
chmod +x setup.sh
```

### Banco de dados corrompido
```bash
# Delete o banco e crie novamente
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 📧 Emails

**Configuração atual:** Console (desenvolvimento)

Para usar emails reais em produção, modifique em `config/settings.py`:

```python
# Substitua:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Por:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'seu-smtp-host.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'seu-email@example.com'
EMAIL_HOST_PASSWORD = 'sua-senha'
```

---

## 🚢 Deployment (Produção)

Para fazer deploy em produção:

1. **Modifique settings.py**
   - `DEBUG = False`
   - Adicione domínios em `ALLOWED_HOSTS`
   - Mude a `SECRET_KEY`

2. **Use um servidor WSGI**
   - Gunicorn, uWSGI, etc.

3. **Banco de dados**
   - Migre para PostgreSQL/MySQL

4. **Arquivos estáticos**
   - Use um serviço CDN ou collectstatic com servidor de arquivos

5. **HTTPS**
   - Configure certificado SSL/TLS

---

## 📚 Referências

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Models](https://docs.djangoproject.com/en/4.2/topics/db/models/)
- [Django Forms](https://docs.djangoproject.com/en/4.2/topics/forms/)
- [Django Views](https://docs.djangoproject.com/en/4.2/topics/http/views/)
- [Django Templates](https://docs.djangoproject.com/en/4.2/topics/templates/)

---

## 👨‍💼 Autor

Desenvolvido como Atividade Prática - SDLC
Curso: Fundamentos de Desenvolvimento de Software

---

## 📄 Licença

Este projeto é fornecido para fins educacionais.

---

**Última atualização:** 11 de maio de 2026

Dúvidas? Consulte a documentação SDLC incluída no projeto!

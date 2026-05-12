# 🏢 Sistema de Reserva de Salas - Projeto Completo SDLC + Django

> **Atividade Prática - Aplicando o SDLC**
> 
> Um sistema profissional de reserva de salas desenvolvido com Django e SQLite, incluindo documentação SDLC completa.

---

## 📦 O Que Está Incluído

### ✅ Documentação SDLC (5 Passos)
```
├── PASSO_1_FASES_SDLC.md               # 7 fases do SDLC
├── PASSO_2_PAPEIS_RESPONSABILIDADES.md # 9 papéis profissionais
├── PASSO_3_REQUISITOS.md               # 15 requisitos levantados
├── PASSO_4_DESIGN_IMPLEMENTACAO.md     # Design + Protótipos + Pseudocódigo
├── PASSO_5_TESTES.md                   # 50+ Casos de teste
└── RELATORIO_FINAL_PASSO4.html         # Relatório Executivo (2 pág)
```

### ✅ Sistema Django Funcional
```
sistema_reservas/
├── config/          # Configurações Django
├── reservas/        # App principal
│   ├── models.py    # 4 modelos de dados
│   ├── views.py     # 16 views
│   ├── forms.py     # 6 formulários
│   └── templates/   # 18 templates HTML
└── static/css/      # CSS responsivo
```

---

### ✅ Ferramentas
```
├── setup.sh                # Script de instalação automática
├── requirements.txt        # Dependências Python
└── manage.py               # Gerenciador Django
```

---

## 🚀 Começar em 3 Passos

### 1️⃣ Configurar Docker
```bash
docker compose down -v
docker compose build --no-cache
docker compose up
```

### 2️⃣ Configurar Superuser
Abra um outro terminal para rodar o comando abaixo
```bash
docker compose exec web python manage.py createsuperuser
```

Preencha os dados:
```sh
Username:
Email:
Password:
```

### 3️⃣ Acessar Sistema
- **Admin**: http://localhost:8000/admin
- **Sistema**: http://localhost:8000

**Pronto!** Sistema funcionando em 5 minutos ✅

---

## ✨ Principais Funcionalidades

✅ **Usuários Comuns**
- Registro e login seguro
- Fazer reservas de salas
- Listar suas reservas
- Cancelar reservas (até 2h antes)
- Ver salas disponíveis

✅ **Administradores**  
- Tudo do usuário comum +
- Gerenciar salas (CRUD)
- Ver todas as reservas
- Cancelar qualquer reserva
- Gerar relatórios
- Visualizar auditoria

✅ **Segurança**
- Autenticação segura
- Validação de conflitos
- Proteção CSRF
- Auditoria completa
- Criptografia de senhas

---

## 🎯 Requisitos Atendidos

| Requisito | Status |
|-----------|--------|
| Autenticação (comum/admin)    | ✅ |
| Fazer reserva para horário    | ✅ |
| Listar reservas               | ✅ |
| Cancelar reserva (admin)      | ✅ |
| Aplicar SDLC                  | ✅ |
| Relatório 2 páginas           | ✅ |
| Código funcionando            | ✅ |

---

## 🎓 Conceitos Aplicados

✅ SDLC (Software Development Life Cycle)
✅ Modelos de Dados Relacionais
✅ Autenticação e Autorização
✅ Validação de Negócio
✅ MVC (Model-View-Controller)
✅ Segurança Web
✅ Design Responsivo
✅ Testes Sistemáticos

---

### Explorar o Código
- Modelos: `sistema_reservas/reservas/models.py`
- Lógica: `sistema_reservas/reservas/views.py`
- Templates: `sistema_reservas/reservas/templates/`


## 🔧 Requisitos Técnicos

- Docker
- Python 3.8+
- pip (gerenciador de pacotes)
- Navegador moderno
- Terminal/CMD

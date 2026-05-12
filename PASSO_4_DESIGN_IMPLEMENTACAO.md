# Passo 4: Design e Implementação do Software

## 4.1 Arquitetura do Sistema

### Arquitetura Geral
```
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE APRESENTAÇÃO                   │
│  (HTML/CSS/JavaScript - React/Vue/Angular)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Tela Login   │  │ Tela Reserva │  │ Tela Admin   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  CAMADA DE APLICAÇÃO                        │
│  (Node.js/Express, Django, Spring Boot, etc.)               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Controladores: Auth, Reservas, Salas, Usuários         │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │ Lógica de Negócio: Validação, Autenticação, Permissões │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │ Serviços: Email, Notificações, Relatórios              │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 CAMADA DE DADOS                             │
│  (PostgreSQL, MySQL, MongoDB)                               │
│  ┌──────────┐  ┌─────────┐  ┌──────────┐  ┌────────────┐    │
│  │ Usuários │  │ Salas   │  │ Reservas │  │ Histórico  │    │ 
│  └──────────┘  └─────────┘  └──────────┘  └────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 4.2 Modelo de Dados

### Entidades Principais

#### USUÁRIO
- `id` (PK): Identificador único
- `email` (UNIQUE): Email do usuário
- `senha_hash`: Senha criptografada
- `nome`: Nome completo
- `tipo`: 'comum' ou 'admin'
- `ativo`: Boolean
- `data_criacao`: Timestamp
- `data_atualizacao`: Timestamp

#### SALA
- `id` (PK): Identificador único
- `nome`: Nome da sala
- `capacidade`: Número de pessoas
- `localizacao`: Localização na empresa
- `recursos`: Descrição dos recursos (projetor, quadro, etc)
- `ativa`: Boolean
- `data_criacao`: Timestamp

#### RESERVA
- `id` (PK): Identificador único
- `usuario_id` (FK): Referência ao usuário
- `sala_id` (FK): Referência à sala
- `data_reserva`: Data da reserva
- `hora_inicio`: Hora de início
- `hora_fim`: Hora de fim
- `motivo`: Descrição da reunião
- `status`: 'ativa', 'cancelada', 'concluída'
- `data_criacao`: Timestamp
- `data_cancelamento`: Timestamp (null se não cancelada)
- `motivo_cancelamento`: Texto (null se não cancelada)

#### AUDITORIA (Histórico)
- `id` (PK): Identificador único
- `usuario_id` (FK): Usuário que fez a ação
- `tipo_acao`: 'criacao_reserva', 'cancelamento', 'login', etc
- `descricao`: Detalhes da ação
- `data_acao`: Timestamp

---

## 4.3 Protótipos de Interface

### Tela 1: Login
```
┌──────────────────────────────────────────┐
│      SISTEMA DE RESERVA DE SALAS         │
├──────────────────────────────────────────┤
│                                          │
│  Email:    [________________________]    │
│                                          │
│  Senha:    [________________________]    │
│                                          │
│  ( ) Lembrar de mim                      |
│                                          │
│           [ ENTRAR ]                     │
│                                          │
│  Não tem conta? [ Criar conta ]          │
│                                          │
└──────────────────────────────────────────┘
```

### Tela 2: Cadastro
```
┌──────────────────────────────────────────┐
│      CRIAR NOVA CONTA                    │
├──────────────────────────────────────────┤
│                                          │
│  Nome:     [________________________]    │
│                                          │
│  Email:    [________________________]    │
│                                          │
│  Senha:    [________________________]    │
│                                          │
│  Confirmar:[________________________]    │
│                                          │
│  [ CRIAR CONTA ]  [ CANCELAR ]           │
│                                          │
└──────────────────────────────────────────┘
```

### Tela 3: Dashboard Principal
```
┌────────────────────────────────────────────────────────────┐
│  RESERVA DE SALAS  [Bem-vindo, João]  [LOGOUT]             │
├────────────────────────────────────────────────────────────┤
│ Menu:                                                      │
│ ├─ [Novas Reservas]  [Minhas Reservas]  [Salas]            │
│ └─ (Admin) [Gerenciar Salas] [Relatórios] [Usuários]       │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  FAZER UMA RESERVA                                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Sala:       [Dropdown ▼]                             │  │
│  │ Data:       [__/__/____]                             │  │
│  │ Hora Início:[__:__] Hora Fim: [__:__]                │  │
│  │ Motivo:     [____________________]                   │  │
│  │                                                      │  │
│  │ Salas disponíveis neste horário:                     │  │
│  │ • Sala A (20 pessoas) - Projetor, Quadro             │  │
│  │ • Sala C (8 pessoas) - Quadro                        │  │
│  │                                                      │  │
│  │ [ RESERVAR ]  [ LIMPAR ]                             │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

### Tela 4: Minhas Reservas
```
┌────────────────────────────────────────────────────────────┐
│  MINHAS RESERVAS                                           │
├────────────────────────────────────────────────────────────┤
│ Filtros: Sala [_______] Data [__/__/____] Status [▼]       │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ * Sala A | 15/05/2026 | 14:00-15:30 | Reunião Projeto      │
│   Status: ATIVA | [ CANCELAR ] | Criada em 11/05/2026      │
│                                                            │
│ * Sala B | 12/05/2026 | 10:00-11:00 | Treinamento          │
│   Status: ATIVA | [ CANCELAR ] | Criada em 10/05/2026      │
│                                                            │
│ * Sala C | 08/05/2026 | 09:00-10:00 | 1:1 Manager          │
│   Status: CONCLUÍDA | Criada em 05/05/2026                 |
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Tela 5: Painel Admin - Todas as Reservas
```
┌────────────────────────────────────────────────────────────┐
│  TODAS AS RESERVAS (ADMIN)                                 │
├────────────────────────────────────────────────────────────┤
│ Filtros: Sala [▼] | Data [__/__] | Usuário [_______] | [  ]│
├────────────────────────────────────────────────────────────┤
│ # │ Usuário  │ Sala │ Data/Hora        │ Status │ Ações    │
│───┼──────────┼──────┼──────────────────┼────────┼──────────│
│1  │ João     │ Sala A│ 15/05 14:00-15:30│ ATIVA │[Cancelar]│
│2  │ Maria    │ Sala B│ 15/05 10:00-11:00│ ATIVA │[Cancelar]│
│3  │ Pedro    │ Sala C│ 14/05 16:00-17:00│ ATIVA │[Cancelar]│
│4  │ Ana      │ Sala A│ 13/05 09:00-10:00│ CANCEL│[Visualiz]│
│                                                            │
│ [◀ Anterior] | Página 1 de 5 | [Próximo ▶]                │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 4.4 Pseudocódigo de Funcionalidades-Chave

### Algoritmo: Verificar Disponibilidade de Sala
```pseudocode
FUNÇÃO verificarDisponibilidadeSala(salaId, data, horaInicio, horaFim)
    INÍCIO
        reservasExistentes = buscarReservasDaSala(salaId, data, status='ATIVA')
        
        PARA CADA reserva EM reservasExistentes FAÇA
            SE (horaInicio < reserva.horaFim) E (horaFim > reserva.horaInicio) ENTÃO
                RETORNAR false  // Conflito encontrado
            FIM SE
        FIM PARA
        
        RETORNAR true  // Sala disponível
    FIM
```

### Algoritmo: Criar Reserva
```pseudocode
FUNÇÃO criarReserva(usuarioId, salaId, data, horaInicio, horaFim, motivo)
    INÍCIO
        // Validações
        SE verificarInputs(salaId, data, horaInicio, horaFim) = false ENTÃO
            RETORNAR ERRO("Dados inválidos")
        FIM SE
        
        SE verificarDisponibilidadeSala(salaId, data, horaInicio, horaFim) = false ENTÃO
            RETORNAR ERRO("Sala indisponível neste horário")
        FIM SE
        
        SE (horaFim - horaInicio) < 15 MINUTOS ENTÃO
            RETORNAR ERRO("Duração mínima: 15 minutos")
        FIM SE
        
        // Criar reserva
        novaReserva = CRIAR {
            usuario_id: usuarioId,
            sala_id: salaId,
            data: data,
            hora_inicio: horaInicio,
            hora_fim: horaFim,
            motivo: motivo,
            status: 'ATIVA',
            data_criacao: AGORA()
        }
        
        salvarNoBancoDados(novaReserva)
        enviarEmailConfirmacao(usuarioId, novaReserva)
        registrarAuditoria(usuarioId, 'CRIACAO_RESERVA', novaReserva.id)
        
        RETORNAR SUCESSO("Reserva criada com sucesso")
    FIM
```

### Algoritmo: Cancelar Reserva
```pseudocode
FUNÇÃO cancelarReserva(usuarioId, reservaId, motivoCancelamento)
    INÍCIO
        reserva = buscarReserva(reservaId)
        usuario = buscarUsuario(usuarioId)
        
        // Validar permissões
        SE usuario.tipo != 'admin' E reserva.usuario_id != usuarioId ENTÃO
            RETORNAR ERRO("Sem permissão para cancelar esta reserva")
        FIM SE
        
        // Validar antecedência mínima
        tempoRestante = (reserva.data + reserva.hora_inicio) - AGORA()
        SE usuario.tipo != 'admin' E tempoRestante < 2 HORAS ENTÃO
            RETORNAR ERRO("Cancelamento deve ser feito 2 horas antes")
        FIM SE
        
        // Cancelar
        reserva.status = 'CANCELADA'
        reserva.data_cancelamento = AGORA()
        reserva.motivo_cancelamento = motivoCancelamento
        
        salvarNoBancoDados(reserva)
        enviarEmailCancelamento(reserva.usuario_id, reserva)
        registrarAuditoria(usuarioId, 'CANCELAMENTO_RESERVA', reservaId)
        
        RETORNAR SUCESSO("Reserva cancelada")
    FIM
```

### Algoritmo: Autenticação
```pseudocode
FUNÇÃO autenticar(email, senha)
    INÍCIO
        usuario = buscarUsuarioPorEmail(email)
        
        SE usuario = NULL ENTÃO
            RETORNAR ERRO("Email ou senha incorretos")
        FIM SE
        
        SE verificarHash(senha, usuario.senha_hash) = false ENTÃO
            registrarTentativaFalha(email)
            RETORNAR ERRO("Email ou senha incorretos")
        FIM SE
        
        SE usuario.ativo = false ENTÃO
            RETORNAR ERRO("Usuário inativo")
        FIM SE
        
        token = gerarTokenJWT(usuario.id, usuario.tipo)
        registrarLogin(usuario.id)
        
        RETORNAR {token, usuario.id, usuario.tipo}
    FIM
```

---

## 4.5 Etapas de Implementação

### Fase 1: Configuração do Ambiente
1. Configurar ambiente de desenvolvimento (IDE, versões de ferramentas)
2. Criar estrutura de pastas do projeto
3. Inicializar repositório Git
4. Configurar banco de dados (desenvolvimento, teste, produção)

### Fase 2: Backend - Autenticação e Segurança
1. Implementar modelo de dados (tabelas no banco)
2. Criar endpoints de autenticação (login, registro)
3. Implementar JWT e sessions
4. Adicionar middleware de autenticação
5. Implementar criptografia de senhas (bcrypt)
6. Testes unitários de autenticação

### Fase 3: Backend - Funcionalidades Core
1. Implementar CRUD de Salas (Admin)
2. Implementar CRUD de Reservas
3. Implementar lógica de validação de conflitos
4. Implementar sistema de permissões (Admin vs Comum)
5. Implementar endpoints de listagem com filtros
6. Testes de lógica de negócio

### Fase 4: Backend - Serviços Complementares
1. Implementar serviço de email (confirmações e notificações)
2. Implementar sistema de auditoria (logs)
3. Implementar geração de relatórios
4. Validação de dados de entrada
5. Tratamento de erros robusto

### Fase 5: Frontend - Interface Básica
1. Criar telas de login e registro
2. Implementar formulário de reserva
3. Implementar listagem de minhas reservas
4. Implementar painel de cancelamento
5. Integração básica com API

### Fase 6: Frontend - Funcionalidades Avançadas
1. Implementar painel admin com todas as reservas
2. Implementar gerenciamento de salas (admin)
3. Adicionar filtros e buscas
4. Implementar relatórios visuais
5. Validações no frontend

### Fase 7: Testes e Qualidade
1. Testes unitários (backend e frontend)
2. Testes de integração
3. Testes de usabilidade
4. Testes de segurança (penetration testing)
5. Testes de performance e carga

### Fase 8: Deploy e Manutenção
1. Preparar ambiente de produção
2. Configurar CI/CD (integração contínua)
3. Deploy inicial
4. Monitoramento e logs
5. Suporte a usuários

# Acessando Atividade Completa e código fonte

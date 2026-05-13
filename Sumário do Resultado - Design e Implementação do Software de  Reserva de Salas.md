## Sumário do Resultado - Design e Implementação do Software de  Reserva de Salas
**Autor:** Alexandre Gomes   **Data:** 13/05/2026   

### Passo 1: Identificação das fases do SDLC

| Fase | Atividades no projeto |
|---|---|
| Levantamento de Requisitos | Identificar as necessidades dos usuarios e administradores, como login, reserva de salas, listagem e cancelamento por admin. |
| Analise | Avaliar regras de negocio, restricoes e riscos, principalmente conflitos de horario, perfis de acesso e seguranca dos dados. |
| Design | Definir arquitetura, telas, modelo de dados e fluxo do sistema antes da codificacao. |
| Implementacao | Desenvolver autenticacao, cadastro de salas, criacao de reservas, listagem e cancelamento. |
| Testes | Validar login, reservas validas, reservas com conflito, permissoes de admin e exibicao correta das reservas. |
| Implantacao | Preparar o ambiente, configurar banco de dados e disponibilizar o acesso aos usuarios. |
| Manutencao | Corrigir falhas, monitorar o uso, melhorar funcionalidades e adaptar o sistema a novas necessidades. |

### Passo 2. Definição dos papéis e responsabilidades

| Papel | Responsabilidades |
|---|---|
| Product Owner | Define prioridades, valida requisitos e garante que o sistema atenda as necessidades dos usuarios. |
| Analista de Requisitos | Coleta, organiza e documenta requisitos funcionais e nao funcionais. |
| Arquiteto de Software | Define a estrutura tecnica da solucao, incluindo camadas, tecnologias e banco de dados. |
| Designer UX/UI | Cria o fluxo das telas e busca uma interface simples, clara e facil de usar. |
| Desenvolvedor Backend | Implementa regras de negocio, autenticacao, permissoes, reservas e validacao de conflitos. |
| Desenvolvedor Frontend | Desenvolve as telas de login, reserva, listagem e painel administrativo. |
| Testador/QA | Planeja e executa testes para validar funcionalidades, seguranca, permissoes e conflitos. |
| DevSecOps | Apoia implantacao, automacao, monitoramento e boas praticas de seguranca. |

### Passo 3: Levantamento de requisitos do software

| Requisitos funcionais | Descricao |
|---|---|
| Autenticacao de usuarios | Permitir login com email e senha, diferenciando usuarios comuns e administradores. |
| Reserva de salas | Permitir que usuarios reservem uma sala informando data, horario de inicio, horario de fim e motivo. |
| Gerenciamento de conflitos | Impedir reservas duplicadas para a mesma sala no mesmo intervalo de horario. |
| Listagem de reservas | Permitir que usuarios comuns vejam suas reservas e administradores vejam todas. |
| Cancelamento de reservas | Permitir cancelamento apenas por usuarios administradores, mantendo historico da acao. |
| Notificacoes por email | Enviar confirmacoes de reserva e avisos de cancelamento aos usuarios envolvidos. |
| Gerenciamento de salas | Permitir que administradores cadastrem, editem e desativem salas. |

| Requisitos nao funcionais | Descricao |
|---|---|
| Seguranca | Armazenar senhas com criptografia, proteger sessoes e validar permissoes de acesso. |
| Usabilidade | Oferecer interface simples, com mensagens claras para sucesso, erro e conflito de horario. |
| Desempenho | Consultar disponibilidade e listar reservas de forma rapida, mesmo com muitos registros. |
| Disponibilidade | Manter o sistema acessivel durante o horario de uso da empresa. |
| Auditoria | Registrar operacoes importantes, como criacao e cancelamento de reservas. |
| Manutenibilidade | Organizar o codigo em camadas e manter documentacao para facilitar futuras melhorias. |

### Passo 4: Design e implementacao do software

#### 4.1 Esboco da Interface

```text
SISTEMA DE RESERVA DE SALAS

[Tela de Login]
Email: [________________]   Senha: [________________]   [Entrar]

[Tela Principal]
Usuario: Alexandre                 Perfil: Admin
------------------------------------------------
[Nova Reserva] [Minhas Reservas] [Painel Admin]

Nova Reserva:
Sala:        [Sala A v]
Data:        [13/05/2026]
Inicio/Fim:  [14:00] ate [15:00]
Motivo:      [Reuniao de projeto] [Reservar]

Minhas Reservas:
Sala A | 13/05/2026 | 14:00-15:00 | Ativa

Painel Admin:
Usuario | Sala | Data/Hora        | Status | Acao
Joao    | A    | 13/05 14:00-15:00| Ativa  | [Cancelar]
```

#### 4.2 Componentes do Programa

| Componente | Funcao |
|---|---|
| Login | Autentica o usuario e identifica seu perfil: comum ou admin. |
| Nova Reserva | Permite escolher sala, data, horario e motivo da reuniao. |
| Minhas Reservas | Lista as reservas do usuario autenticado. |
| Painel Admin | Exibe todas as reservas e permite cancelamento pelo administrador. |
| Banco de Dados | Guarda usuarios, salas, reservas e historico de acoes. |

#### 4.3 Regra principal em pseudocodigo

```pseudocode
FUNCAO verificarDisponibilidade(sala, data, inicio, fim)
    reservas = buscarReservasAtivas(sala, data)

    PARA CADA reserva EM reservas
        SE inicio < reserva.hora_fim E fim > reserva.hora_inicio
            RETORNAR falso
        FIM SE
    FIM PARA

    RETORNAR verdadeiro
FIM FUNCAO

FUNCAO reservarSala(usuario, sala, data, inicio, fim)
    SE verificarDisponibilidade(sala, data, inicio, fim) = falso
        RETORNAR "Sala indisponivel neste horario"
    FIM SE

    salvarReserva(usuario, sala, data, inicio, fim)
    RETORNAR "Reserva criada com sucesso"
FIM FUNCAO
```

### Passo 5: Testes do software

| Cenario de teste | O que sera validado | Resultado esperado |
|---|---|---|
| Login valido | Usuario informa email e senha corretos. | Acesso liberado conforme o perfil do usuario. |
| Login invalido | Usuario informa credenciais incorretas. | Sistema bloqueia o acesso e exibe mensagem de erro. |
| Reserva valida | Usuario reserva uma sala disponivel em data e horario validos. | Reserva criada com status ativa. |
| Reserva com conflito | Usuario tenta reservar sala ja ocupada no mesmo horario. | Sistema impede a reserva e informa indisponibilidade. |
| Listagem do usuario | Usuario comum acessa suas reservas. | Apenas suas proprias reservas sao exibidas. |
| Listagem do admin | Administrador acessa o painel administrativo. | Todas as reservas do sistema sao exibidas. |
| Cancelamento por admin | Administrador cancela uma reserva existente. | Reserva muda para cancelada e a acao e registrada. |
| Cancelamento por usuario comum | Usuario comum tenta cancelar reserva pelo painel admin. | Sistema nega a acao por falta de permissao. |
| Notificacao por email | Reserva ou cancelamento e realizado. | Usuario recebe mensagem de confirmacao ou cancelamento. |

# Passo 1: Identificação das Fases do SDLC

## Fases Aplicadas ao Software de Reserva de Salas

### 1. Levantamento de Requisitos
**Atividades:**
- Reuniões com stakeholders (usuários finais, administradores)
- Coleta de necessidades e expectativas
- Definição do escopo do projeto
- Documentação de requisitos funcionais e não-funcionais

**Aplicação:** Identificar que o sistema precisa de autenticação, reservas, listagem e cancelamento (apenas admin).

### 2. Análise
**Atividades:**
- Análise de viabilidade técnica e econômica
- Identificação de dependências e restrições
- Avaliação de riscos
- Definição de arquitetura de alto nível

**Aplicação:** Avaliar tecnologias para implementação (banco de dados, framework web), definir tratamento de conflitos de horários.

### 3. Design (Projeto)
**Atividades:**
- Criação de modelos de dados (ER diagrams)
- Design da arquitetura do sistema
- Prototipagem de interfaces de usuário
- Especificação de componentes e módulos

**Aplicação:** Desenhar telas de login, reserva, listagem; modelar entidades (Usuário, Sala, Reserva).

### 4. Desenvolvimento (Implementação)
**Atividades:**
- Codificação conforme especificações de design
- Testes unitários
- Integração de componentes
- Documentação do código

**Aplicação:** Implementar backend (APIs, autenticação), frontend (interfaces), e banco de dados.

### 5. Testes
**Atividades:**
- Testes funcionais (casos de uso, fluxos)
- Testes não-funcionais (performance, segurança)
- Testes de integração
- Relatório de defeitos e correções

**Aplicação:** Validar reservas com conflitos, permissões de cancelamento, validação de dados.

### 6. Deployment (Implantação)
**Atividades:**
- Preparação do ambiente de produção
- Migração de dados
- Treinamento de usuários
- Plano de rollback

**Aplicação:** Publicar sistema em servidor web, criar base de dados de produção.

### 7. Manutenção
**Atividades:**
- Monitoramento de performance
- Suporte a usuários
- Correção de bugs
- Melhorias e atualizações

**Aplicação:** Acompanhar uso do sistema, corrigir problemas reportados, implementar novas funcionalidades.

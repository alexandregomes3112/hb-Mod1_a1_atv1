# Passo 2: Definição dos Papéis e Responsabilidades

## Papéis no Projeto de Reserva de Salas

### 1. Gerente de Projeto
**Responsabilidades:**
- Planejamento e agendamento do projeto
- Definição de prazos e milestones
- Gerenciamento de riscos
- Comunicação com stakeholders
- Acompanhamento do progresso e qualidade

**Aplicação:** Assegurar que o software seja entregue no prazo com qualidade, mediando entre equipe técnica e clientes.

### 2. Analista de Requisitos
**Responsabilidades:**
- Coleta e análise de requisitos com stakeholders
- Documentação clara dos requisitos funcionais e não-funcionais
- Validação de requisitos com interessados
- Identificação de conflitos e ambiguidades
- Criação de especificações detalhadas

**Aplicação:** Definir exatamente o que o sistema de reservas deve fazer, validar que admin pode cancelar mas usuários comuns não.

### 3. Arquiteto de Software
**Responsabilidades:**
- Design da arquitetura geral do sistema
- Escolha de tecnologias e frameworks
- Definição de padrões de design
- Garantir escalabilidade e performance
- Revisar implementações críticas

**Aplicação:** Decidir usar padrão MVC, banco de dados relacional, autenticação via JWT, etc.

### 4. Designer de UX/UI
**Responsabilidades:**
- Criar protótipos de interfaces
- Design visual e experiência do usuário
- Testes de usabilidade
- Documentação de componentes e estilos
- Garantir acessibilidade

**Aplicação:** Desenhar telas intuitivas para login, busca e reserva de salas, considerando fluxos de usuários diferentes.

### 5. Desenvolvedor Backend
**Responsabilidades:**
- Implementação da lógica de negócios
- Desenvolvimento de APIs e serviços
- Integração com banco de dados
- Testes unitários
- Documentação técnica

**Aplicação:** Implementar autenticação, validação de conflitos de horários, lógica de permissões (admin vs usuário comum).

### 6. Desenvolvedor Frontend
**Responsabilidades:**
- Implementação das interfaces de usuário
- Integração com APIs
- Testes de compatibilidade (navegadores, dispositivos)
- Otimização de performance
- Tratamento de erros e feedback ao usuário

**Aplicação:** Construir formulários de login e reserva, listar reservas, interface de cancelamento.

### 7. Testador (QA)
**Responsabilidades:**
- Criação de planos de testes
- Execução de testes funcionais e não-funcionais
- Documentação de bugs e defeitos
- Validação de correções
- Testes de regressão

**Aplicação:** Verificar se reservas com horários conflitantes são recusadas, se apenas admins conseguem cancelar, validar dados inseridos.

### 8. Administrador de Banco de Dados
**Responsabilidades:**
- Modelagem do banco de dados
- Criação e manutenção de schemas
- Backup e disaster recovery
- Otimização de queries
- Segurança de dados

**Aplicação:** Estruturar tabelas de Usuários, Salas, Reservas com relacionamentos adequados, criar índices para performance.

### 9. Especialista em Segurança
**Responsabilidades:**
- Análise de vulnerabilidades
- Implementação de controles de segurança
- Revisão de código para brechas
- Testes de penetração
- Conformidade com regulamentações

**Aplicação:** Validar senhas fortes, proteger contra SQL injection, garantir que apenas usuários autenticados acessem reservas, criptografia de dados sensíveis.

# Passo 5: Testes do Software

## Plano de Testes - Sistema de Reserva de Salas

---

## 5.1 Estratégia de Testes

### Níveis de Teste
- **Testes Unitários**: Funções individuais de validação, autenticação, etc
- **Testes de Integração**: Integração entre componentes (API + BD, Email service)
- **Testes Funcionais**: Fluxos completos de usuário (login → reserva → confirmação)
- **Testes de Aceitação**: Validação contra requisitos do usuário
- **Testes de Performance**: Tempo de resposta, carga do sistema
- **Testes de Segurança**: Validação contra SQL injection, XSS, etc

---

## 5.2 Casos de Teste - Autenticação

### CT-001: Login com Credenciais Válidas
- **Pré-condição:** Usuário cadastrado com email e senha válidos
- **Passos:**
  1. Acessar tela de login
  2. Inserir email válido
  3. Inserir senha correta
  4. Clicar em "Entrar"
- **Resultado Esperado:** Usuário é autenticado e redirecionado ao dashboard
- **Prioridade:** Alta

### CT-002: Login com Email Inválido
- **Pré-condição:** Email não existe no sistema
- **Passos:**
  1. Acessar tela de login
  2. Inserir email não cadastrado
  3. Inserir qualquer senha
  4. Clicar em "Entrar"
- **Resultado Esperado:** Mensagem de erro "Email ou senha incorretos"
- **Prioridade:** Alta

### CT-003: Login com Senha Incorreta
- **Pré-condição:** Usuário existe, mas senha é incorreta
- **Passos:**
  1. Acessar tela de login
  2. Inserir email válido
  3. Inserir senha incorreta
  4. Clicar em "Entrar"
- **Resultado Esperado:** Mensagem de erro "Email ou senha incorretos"
- **Prioridade:** Alta

### CT-004: Logout
- **Pré-condição:** Usuário autenticado
- **Passos:**
  1. Clicar em "Logout"
  2. Confirmar logout
- **Resultado Esperado:** Usuário é desconectado e redirecionado para tela de login
- **Prioridade:** Alta

### CT-005: Expiração de Sessão
- **Pré-condição:** Usuário autenticado
- **Passos:**
  1. Autenticar usuário
  2. Aguardar 30 minutos sem atividade
  3. Tentar acessar página protegida
- **Resultado Esperado:** Sessão expira e usuário é redirecionado para login
- **Prioridade:** Média

### CT-006: Cadastro com Email Duplicado
- **Pré-condição:** Email já existe no sistema
- **Passos:**
  1. Acessar tela de registro
  2. Inserir email já cadastrado
  3. Inserir outros dados válidos
  4. Clicar em "Criar Conta"
- **Resultado Esperado:** Erro "Email já cadastrado"
- **Prioridade:** Alta

### CT-007: Cadastro com Senha Fraca
- **Pré-condição:** Nenhuma
- **Passos:**
  1. Acessar tela de registro
  2. Inserir senha com menos de 8 caracteres
  3. Clicar em "Criar Conta"
- **Resultado Esperado:** Erro "Senha deve ter mínimo 8 caracteres"
- **Prioridade:** Alta

---

## 5.3 Casos de Teste - Reservas

### CT-101: Reservar Sala com Sucesso
- **Pré-condição:** Usuário autenticado, sala disponível
- **Passos:**
  1. Acessar "Fazer Reserva"
  2. Selecionar sala disponível
  3. Inserir data futura
  4. Inserir horário disponível (ex: 14:00-15:00)
  5. Inserir motivo
  6. Clicar "Reservar"
- **Resultado Esperado:** 
  - Mensagem de sucesso
  - Email de confirmação enviado
  - Reserva aparece na lista pessoal
- **Prioridade:** Alta

### CT-102: Reservar Sala com Conflito de Horário
- **Pré-condição:** 
  - Usuário autenticado
  - Sala tem reserva de 14:00-15:00
- **Passos:**
  1. Acessar "Fazer Reserva"
  2. Selecionar a mesma sala
  3. Tentar reservar de 14:30-15:30
- **Resultado Esperado:** 
  - Erro "Sala indisponível neste horário"
  - Salas alternativas são sugeridas
- **Prioridade:** Alta

### CT-103: Reserva com Duração Mínima
- **Pré-condição:** Usuário autenticado
- **Passos:**
  1. Acessar "Fazer Reserva"
  2. Selecionar sala
  3. Inserir horário com duração de 10 minutos
  4. Clicar "Reservar"
- **Resultado Esperado:** Erro "Duração mínima é 15 minutos"
- **Prioridade:** Média

### CT-104: Reservar Sala para Data Passada
- **Pré-condição:** Usuário autenticado
- **Passos:**
  1. Acessar "Fazer Reserva"
  2. Selecionar sala
  3. Inserir data no passado
  4. Clicar "Reservar"
- **Resultado Esperado:** Erro "Data inválida"
- **Prioridade:** Média

### CT-105: Listar Reservas - Usuário Comum
- **Pré-condição:** Usuário comum autenticado com 3 reservas
- **Passos:**
  1. Acessar "Minhas Reservas"
- **Resultado Esperado:** 
  - Apenas as 3 reservas do usuário são exibidas
  - Informações corretas (sala, data, horário)
- **Prioridade:** Alta

### CT-106: Listar Reservas - Admin
- **Pré-condição:** Admin autenticado, há 10+ reservas no sistema
- **Passos:**
  1. Acessar "Todas as Reservas"
- **Resultado Esperado:** 
  - Todas as reservas são exibidas
  - Informações do usuário responsável aparecem
  - Paginação funciona
- **Prioridade:** Alta

### CT-107: Filtrar Reservas por Data
- **Pré-condição:** Múltiplas reservas em datas diferentes
- **Passos:**
  1. Acessar listagem de reservas
  2. Filtrar por data específica
- **Resultado Esperado:** Apenas reservas da data selecionada aparecem
- **Prioridade:** Média

---

## 5.4 Casos de Teste - Cancelamento

### CT-201: Cancelar Própria Reserva com Antecedência
- **Pré-condição:** 
  - Usuário comum com reserva em 3 horas
- **Passos:**
  1. Acessar "Minhas Reservas"
  2. Clicar "Cancelar" em sua reserva
  3. Confirmar cancelamento
- **Resultado Esperado:** 
  - Reserva muda para status "Cancelada"
  - Email de cancelamento é enviado
- **Prioridade:** Alta

### CT-202: Cancelar Reserva com Menos de 2 Horas
- **Pré-condição:** 
  - Usuário comum com reserva em 1 hora
- **Passos:**
  1. Acessar "Minhas Reservas"
  2. Tentar clicar "Cancelar"
- **Resultado Esperado:** 
  - Botão desabilitado ou erro "Cancelamento deve ser 2 horas antes"
- **Prioridade:** Alta

### CT-203: Usuário Comum Tenta Cancelar Reserva de Outro
- **Pré-condição:** 
  - Reserva criada por usuário A
  - Usuário B autenticado
- **Passos:**
  1. Usuário B tenta acessar cancelamento da reserva
- **Resultado Esperado:** 
  - Acesso negado
  - Erro "Sem permissão"
- **Prioridade:** Alta

### CT-204: Admin Cancela Qualquer Reserva
- **Pré-condição:** 
  - Admin autenticado
  - Existe reserva de qualquer usuário
- **Passos:**
  1. Admin acessa "Todas as Reservas"
  2. Clica "Cancelar" em qualquer reserva
  3. Confirma
- **Resultado Esperado:** 
  - Qualquer reserva é cancelada
  - Sem restrição de horário
- **Prioridade:** Alta

---

## 5.5 Casos de Teste - Controle de Acesso

### CT-301: Admin Acessa Painel Admin
- **Pré-condição:** Admin autenticado
- **Passos:**
  1. Acessar dashboard
- **Resultado Esperado:** Opções de admin são visíveis
- **Prioridade:** Alta

### CT-302: Usuário Comum Não Acessa Painel Admin
- **Pré-condição:** Usuário comum autenticado
- **Passos:**
  1. Tentar acessar URL de gerenciamento de salas (/admin/salas)
- **Resultado Esperado:** Acesso negado, erro 403
- **Prioridade:** Alta

### CT-303: Admin Cria Nova Sala
- **Pré-condição:** Admin autenticado
- **Passos:**
  1. Acessar "Gerenciar Salas"
  2. Clicar "Adicionar Sala"
  3. Preencher dados (nome, capacidade, recursos)
  4. Clicar "Salvar"
- **Resultado Esperado:** 
  - Sala é criada
  - Aparece na lista de disponíveis
- **Prioridade:** Alta

### CT-304: Usuário Comum Não Consegue Criar Sala
- **Pré-condição:** Usuário comum autenticado
- **Passos:**
  1. Tentar acessar gerenciamento de salas
- **Resultado Esperado:** Acesso negado
- **Prioridade:** Alta

---

## 5.6 Testes de Segurança

### CT-401: SQL Injection
- **Teste:** Inserir `'; DROP TABLE reservas; --` no campo de email
- **Resultado Esperado:** Entrada é sanitizada, sem dano ao banco
- **Prioridade:** Crítica

### CT-402: XSS (Cross-Site Scripting)
- **Teste:** Inserir `<script>alert('XSS')</script>` no campo motivo
- **Resultado Esperado:** Script é escapado, não executa
- **Prioridade:** Crítica

### CT-403: CSRF (Cross-Site Request Forgery)
- **Teste:** Tentar requisição sem token CSRF
- **Resultado Esperado:** Requisição é rejeitada
- **Prioridade:** Alta

### CT-404: Força Bruta
- **Teste:** 100 tentativas de login com senha errada
- **Resultado Esperado:** Conta é temporariamente bloqueada
- **Prioridade:** Média

---

## 5.7 Testes de Performance

### CT-501: Tempo de Login
- **Teste:** Registrar tempo de resposta do login
- **Resultado Esperado:** Menor que 2 segundos
- **Prioridade:** Média

### CT-502: Listagem com Muitos Registros
- **Teste:** Listar 10.000 reservas
- **Resultado Esperado:** Página carrega em menos de 5 segundos
- **Prioridade:** Média

### CT-503: Validação de Conflitos
- **Teste:** Verificar disponibilidade com 10.000 reservas existentes
- **Resultado Esperado:** Resposta em menos de 500ms
- **Prioridade:** Média

---

## 5.8 Relatório de Testes

### Estrutura do Relatório de Testes
```
Data de Execução: [DATA]
Versão do Sistema: [VERSÃO]
Ambiente: [DEV/TEST/PROD]
Testador: [NOME]

Resumo:
- Total de Testes: XX
- Aprovados: XX (XX%)
- Falhados: XX (XX%)
- Bloqueados: XX

Casos com Falha:
- [CT-XXX]: Descrição do problema
  Severidade: [Crítica/Alta/Média/Baixa]
  
Bugs Reportados:
- BUG-001: [Descrição]
  Passos para reproduzir: [...]
  Impacto: [...]
```

---

## 5.9 Ciclo de Testes

1. **Testes Unitários** (Desenvolvimento)
   - Executados a cada commit
   - Cobertura mínima: 80%

2. **Testes de Integração** (Antes do Release)
   - Banco de dados real
   - Todos os componentes integrados

3. **Testes Funcionais** (QA)
   - Fluxos completos de usuário
   - Casos de sucesso e erro

4. **Testes de Regressão**
   - Após correção de bugs
   - Antes de cada release

5. **Testes de Aceitação**
   - Validação com usuários reais
   - Aprovação final

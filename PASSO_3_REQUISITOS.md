# Passo 3: Levantamento de Requisitos do Software

## Requisitos Funcionais

### RF1: Autenticação de Usuários
- O sistema deve permitir o login de usuários com email e senha
- O sistema deve diferenciar entre usuários comuns e administradores
- Sessões devem expirar após 30 minutos de inatividade
- O sistema deve permitir logout de usuários

**Critérios de Aceitação:**
- Usuários com credenciais válidas conseguem acessar o sistema
- Usuários com credenciais inválidas recebem mensagem de erro
- Usuários comuns têm privilégios limitados
- Admins têm acesso a todas as funcionalidades

### RF2: Cadastro de Usuários
- O sistema deve permitir o registro de novos usuários (apenas comum)
- Deve validar email único
- Deve validar força de senha mínima

**Critérios de Aceitação:**
- Novo usuário consegue se registrar com email e senha válidos
- Sistema recusa emails duplicados
- Senhas fracas são rejeitadas

### RF3: Gerenciamento de Salas
- Apenas admins podem adicionar, editar ou remover salas
- Cada sala deve ter: nome, capacidade, localização, recursos (projetor, whiteboard, etc)
- Sistema deve exibir disponibilidade de cada sala

**Critérios de Aceitação:**
- Admin consegue criar nova sala com todos os dados
- Usuários comuns não conseguem criar salas
- Salas aparecem com disponibilidade correta

### RF4: Reserva de Salas
- Usuários comuns e admins podem fazer reservas
- Deve selecionar: sala, data, horário de início e fim
- Sistema deve validar conflitos de horários
- Reserva bem-sucedida gera confirmação por email

**Critérios de Aceitação:**
- Usuário consegue reservar sala em horário disponível
- Sistema rejeita reservas que conflitam com existentes
- Email de confirmação é enviado
- Reservas com menos de 15 min de duração são recusadas

### RF5: Listagem de Reservas
- Usuários comuns veem apenas suas próprias reservas
- Admins veem todas as reservas do sistema
- Deve mostrar: sala, data, horário, usuário responsável, status
- Deve permitir filtros por data e sala

**Critérios de Aceitação:**
- Usuário comum vê apenas suas reservas
- Admin vê todas as reservas
- Filtros funcionam corretamente
- Informações são exibidas de forma clara

### RF6: Cancelamento de Reservas
- Apenas admins podem cancelar qualquer reserva
- Usuários comuns podem cancelar apenas suas próprias reservas
- Cancelamento deve enviar email de notificação
- Reservas não podem ser canceladas com menos de 2 horas de antecedência

**Critérios de Aceitação:**
- Admin consegue cancelar qualquer reserva
- Usuário comum consegue cancelar sua reserva com antecedência mínima
- Sistema rejeita cancelamento muito próximo do horário
- Email de cancelamento é enviado

### RF7: Relatórios
- Admins podem gerar relatórios de uso de salas
- Relatório deve mostrar: taxa de ocupação, horários mais procurados, salas mais utilizadas

**Critérios de Aceitação:**
- Relatórios são gerados com dados precisos
- Admins conseguem filtrar por período

---

## Requisitos Não-Funcionais

### RNF1: Segurança
- Senhas devem ser criptografadas usando hash (bcrypt ou similar)
- Sistema deve proteger contra SQL injection
- Acesso às funcionalidades restritas deve ser validado
- Dados de usuários devem ser protegidos contra acesso não autorizado

### RNF2: Performance
- Página de login deve carregar em menos de 2 segundos
- Listagem de reservas deve ser rápida mesmo com muitos registros (índices no BD)
- Validação de conflitos deve ser executada em tempo real

### RNF3: Disponibilidade
- Sistema deve estar disponível 99% do tempo (exceto manutenção)
- Banco de dados deve ter backup diário
- Sistema deve ser recuperável em caso de falha (plano de disaster recovery)

### RNF4: Usabilidade
- Interface deve ser intuitiva para usuários sem experiência técnica
- Sistema deve funcionar em navegadores modernos (Chrome, Firefox, Safari, Edge)
- Deve ser responsivo (funcionar em desktop e mobile)
- Mensagens de erro devem ser claras e orientar o usuário

### RNF5: Manutenibilidade
- Código deve seguir padrões de design reconhecidos
- Documentação técnica deve ser mantida atualizada
- Logs detalhados devem registrar operações críticas
- Sistema deve ser facilmente extensível para futuras funcionalidades

### RNF6: Compatibilidade
- Deve funcionar em navegadores atualizados
- Deve ser compatível com diferentes sistemas operacionais
- API deve ser versionada para futuras mudanças

### RNF7: Escalabilidade
- Arquitetura deve suportar crescimento de usuários
- Banco de dados deve ser preparado para crescimento de dados
- Sistema deve permitir adição de novas salas sem impacto

### RNF8: Conformidade Legal
- LGPD: Proteção de dados pessoais de usuários
- Política de privacidade e termos de uso devem ser claros
- Direito ao esquecimento: possibilidade de deletar dados do usuário

### RNF9: Notificações
- Emails de confirmação e cancelamento devem ser enviados corretamente
- Sistema deve ser tolerante a falhas de envio (retry automático)

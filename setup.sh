#!/bin/bash

# Script de Setup do Sistema de Reservas com Django

echo "========================================"
echo "Setup: Sistema de Reserva de Salas"
echo "========================================"
echo ""

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. Criar ambiente virtual
echo -e "${BLUE}1. Criando ambiente virtual...${NC}"
python3 -m venv venv
source venv/bin/activate

# 2. Instalar dependências
echo -e "${BLUE}2. Instalando dependências...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# 3. Executar migrações
echo -e "${BLUE}3. Executando migrações do banco de dados...${NC}"
cd sistema_reservas
python manage.py makemigrations
python manage.py migrate

# 4. Criar superusuário
echo -e "${BLUE}4. Criando superusuário (admin)...${NC}"
echo "Você será solicitado a criar um superusuário"
python manage.py createsuperuser

# 5. Coletar arquivos estáticos
echo -e "${BLUE}5. Coletando arquivos estáticos...${NC}"
python manage.py collectstatic --noinput

# 6. Criar dados de exemplo (opcional)
echo -e "${BLUE}6. Criando dados de exemplo...${NC}"
python manage.py shell << END
from reservas.models import Sala

# Criar salas de exemplo
salas_exemplo = [
    {'nome': 'Sala de Conferência A', 'capacidade': 20, 'localizacao': 'Andar 1 - Bloco A', 'recursos': 'Projetor, Quadro Branco, TV 55", Ar-condicionado'},
    {'nome': 'Sala de Reunião B', 'capacidade': 8, 'localizacao': 'Andar 2 - Bloco B', 'recursos': 'Quadro Branco, Mesa redonda'},
    {'nome': 'Auditório', 'capacidade': 100, 'localizacao': 'Térreo', 'recursos': 'Palco, Projetor, Sistema de Som, Ar-condicionado'},
    {'nome': 'Sala de Treinamento', 'capacidade': 30, 'localizacao': 'Andar 3 - Bloco C', 'recursos': 'Computadores, Projetor, Quadro Branco'},
]

for sala_data in salas_exemplo:
    sala, created = Sala.objects.get_or_create(
        nome=sala_data['nome'],
        defaults={
            'capacidade': sala_data['capacidade'],
            'localizacao': sala_data['localizacao'],
            'recursos': sala_data['recursos'],
            'ativa': True
        }
    )
    if created:
        print(f"✓ Sala '{sala.nome}' criada")
    else:
        print(f"- Sala '{sala.nome}' já existe")

print("\nDados de exemplo carregados!")
END

echo ""
echo -e "${GREEN}========================================"
echo "Setup concluído com sucesso!"
echo "========================================${NC}"
echo ""
echo "Para iniciar o servidor, execute:"
echo "  cd sistema_reservas"
echo "  python manage.py runserver"
echo ""
echo "Acesse: http://localhost:8000"
echo "Admin:  http://localhost:8000/admin"
echo ""
echo "Credenciais padrão:"
echo "  - Username: (seu email/username)"
echo "  - Password: (sua senha)"
echo ""

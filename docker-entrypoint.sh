#!/bin/bash

set -e

# Wait for database to be ready (if using external DB)
echo "Starting Django application..."

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Load example data if needed
echo "Loading example data..."
python manage.py shell << END
from reservas.models import Sala

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

print("Dados de exemplo carregados!")
END

echo "✓ Setup concluído!"
echo "Sistema disponível em: http://localhost:8000"
echo "Admin em: http://localhost:8000/admin"

# Execute command
exec "$@"

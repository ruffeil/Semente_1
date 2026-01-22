#!/bin/bash
echo "Iniciando recuperação de emergência do SEMENTE_FRAME..."
mkdir -p 01_BUSINESS_STRATEGY 02_SOFTWARE_ARCHITECTURE 03_DATA_ENGINEERING 04_SEGURANCA_PRIVACIDADE 05_INFRAESTRUTURA_NUVEM 06_QUALIDADE_TESTES src/core src/engines src/adapters src/utils tests/unit tests/integration
touch src/__init__.py src/core/__init__.py src/engines/__init__.py src/adapters/__init__.py src/utils/__init__.py
git init
git remote add origin https://github.com/ruffeil/SEMENTE_FRAME_ARCHITECTURE.git
echo "Estrutura de pastas recuperada. Execute 'git pull origin main' para restaurar os arquivos."

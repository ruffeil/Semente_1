# Gerenciamento de Dependências e Ambiente
- **Ferramenta Escolhida:** Conda + Pip (ou Poetry) para isolamento total.
- **Ambiente de Desenvolvimento:** Criação de um ambiente 'semente-env' com Python 3.10+ (estabilidade para ML).
- **Reprodutibilidade:** Uso de 'environment.yml' ou 'pyproject.toml' para garantir que todo desenvolvedor use as mesmas versões de Scikit-Learn, Pandas e PyCaret.
- **Isolamento de Produção:** Uso de Docker Containers para garantir que a nuvem (Azure/AWS) tenha as mesmas bibliotecas do computador local.

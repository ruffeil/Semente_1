# Estrutura do Código Fonte (src/)

- **src/core/**: O "Cérebro". Contém a lógica agnóstica de pipeline, orquestração e contratos.
- **src/engines/**: Onde residem as "Strategies". Cada ramo (Agro, Saúde, Vendas) terá seu motor aqui.
- **src/adapters/**: Conversores de entrada e saída (Leitores de CSV, Conectores de Nuvem, Saída para LLM).
- **src/utils/**: Funções auxiliares (Loggers, Anonimizadores, Validadores de Data).
- **tests/**: Pasta espelhada para garantir 100% de cobertura de código.

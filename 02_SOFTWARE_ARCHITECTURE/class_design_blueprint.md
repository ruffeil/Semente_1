# Blueprint de Classes e Interações

## Camada Core (Agnóstica)
- **Class DataContract:** Valida o schema do CSV contra o dicionário do ramo.
- **Class PipelineOrchestrator:** Coordena a execução das 8 etapas do checklist profissional.
- **Class ReportGenerator:** Interface com o LLM para traduzir métricas em insights.

## Camada Engines (Específica)
- **Abstract Class BaseEngine:** Define o contrato que todos os ramos devem seguir.
- **Class SalesEngine / AgroEngine:** Implementações específicas de modelos e features.

## Camada Adapters (I/O)
- **Class DataLoader:** Gerencia leitura de arquivos (Local/Cloud).
- **Class CloudPublisher:** Gerencia o envio de resultados para a Azure.

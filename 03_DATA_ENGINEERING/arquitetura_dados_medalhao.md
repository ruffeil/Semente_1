# Estrutura de Data Lakehouse
O dado percorrerá três camadas de maturidade:
1. **Camada Bronze (Raw):** Armazenamento do arquivo original (imutável) para auditoria e reprocessamento.
2. **Camada Silver (Cleaned):** Dados limpos, tipados e anonimizados. Prontos para análise estatística.
3. **Camada Gold (Business):** Dados agregados e enriquecidos com features calculadas. Prontos para os modelos de ML.
- **Linhagem (Lineage):** Cada linha de dado terá um ID de rastreio vinculando-a ao arquivo de origem.

-- SCHEMA DO CORE SEMENTE_FRAME v1.0

-- 1. Gestão de Clientes e Tenants
CREATE TABLE IF NOT EXISTS tb_tenants (
    id_tenant SERIAL PRIMARY KEY,
    nm_empresa VARCHAR(100) NOT NULL,
    ds_ramo_atividade VARCHAR(50) NOT NULL, -- Vendas, Agro, Saúde, etc.
    dt_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Camada Bronze: Controle de Ingestão (Auditabilidade)
CREATE TABLE IF NOT EXISTS tb_ingestion_logs (
    id_log SERIAL PRIMARY KEY,
    id_tenant INT REFERENCES tb_tenants(id_tenant),
    nm_arquivo_origem VARCHAR(255) NOT NULL,
    ds_hash_arquivo VARCHAR(64), -- Garantia de imutabilidade
    dt_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    st_processamento VARCHAR(20) DEFAULT 'PENDENTE' -- PENDENTE, SUCESSO, FALHA
);

-- 3. Camada Silver: Dados Higienizados e Validados
-- Nota: Em sistemas de alta performance, esta tabela pode ser dinâmica ou em Data Lake.
CREATE TABLE IF NOT EXISTS tb_silver_data (
    id_silver SERIAL PRIMARY KEY,
    id_log INT REFERENCES tb_ingestion_logs(id_log),
    js_dados_limpos JSONB NOT NULL, -- Guarda o dado validado em formato estruturado
    dt_higienizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Camada Gold: Insights e Resultados de ML
CREATE TABLE IF NOT EXISTS tb_gold_insights (
    id_insight SERIAL PRIMARY KEY,
    id_log INT REFERENCES tb_ingestion_logs(id_log),
    ds_insight_narrativo TEXT, -- Saída do LLM
    js_metricas_tecnicas JSONB, -- R2, F1-Score, MAE
    dt_geracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Segurança: Auditoria de Anonimização (LGPD)
CREATE TABLE IF NOT EXISTS tb_security_logs (
    id_security SERIAL PRIMARY KEY,
    id_log INT REFERENCES tb_ingestion_logs(id_log),
    ds_acao VARCHAR(100), -- ex: 'PII_MASKING', 'DATA_HASHING'
    dt_evento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

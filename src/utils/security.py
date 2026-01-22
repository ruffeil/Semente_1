import hashlib

class SecurityManager:
    @staticmethod
    def mask_pii(df, columns):
        """Anonimiza colunas sensíveis usando Hashing (Fase de Segurança)."""
        df_masked = df.copy()
        for col in columns:
            if col in df_masked.columns:
                df_masked[col] = df_masked[col].apply(
                    lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:12]
                )
        return df_masked

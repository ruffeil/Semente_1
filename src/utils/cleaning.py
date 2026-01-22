import pandas as pd

class DataSanitizer:
    @staticmethod
    def clean(df: pd.DataFrame) -> pd.DataFrame:
        """Fase 2 do Checklist: Limpeza e Qualidade."""
        df = df.drop_duplicates()
        # Preenche nulos numéricos com a mediana
        num_cols = df.select_dtypes(include=['number']).columns
        df[num_cols] = df[num_cols].fillna(df[num_cols].median())
        return df

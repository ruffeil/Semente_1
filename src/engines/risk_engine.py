from src.engines.base import BaseEngine
import pandas as pd

class RiskEngine(BaseEngine):
    def process(self, df: pd.DataFrame) -> dict:
        survival_rate = df['Survived'].mean() * 100
        avg_fare = df['Fare'].mean()
        most_affected_class = df.groupby('Pclass')['Survived'].mean().idxmin()
        
        return {
            "survival_rate": f"{round(survival_rate, 2)}%",
            "avg_fare": round(avg_fare, 2),
            "critical_pclass": int(most_affected_class),
            "total_passengers": len(df)
        }

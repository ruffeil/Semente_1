from abc import ABC, abstractmethod
import pandas as pd

class BaseEngine(ABC):
    """
    Classe base abstrata para garantir que todos os motores SEMENTE
    sigam o mesmo padrão de processamento.
    """
    @abstractmethod
    def process(self, df: pd.DataFrame) -> dict:
        pass

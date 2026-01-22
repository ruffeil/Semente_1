from abc import ABC, abstractmethod
import pandas as pd

class BaseEngine(ABC):
    @abstractmethod
    def process(self, df: pd.DataFrame) -> dict:
        """Todo motor de ramo deve implementar este método de processamento."""
        pass

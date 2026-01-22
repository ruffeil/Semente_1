from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class SalesContract(BaseModel):
    data_venda: date
    id_produto: str
    valor: float = Field(gt=0)
    quantidade: int = Field(gt=0)

class AgroContract(BaseModel):
    id_talhao: str
    umidade_solo: float = Field(ge=0, le=100)
    ndvi_index: float = Field(ge=-1, le=1)
    precipitacao_mm: float = Field(ge=0)
    data_leitura: date

class HealthContract(BaseModel):
    paciente_id: str
    idade: int = Field(gt=0)
    pressao_sistolica: int
    nivel_glicose: float
    data_exame: date

class LogisticsContract(BaseModel):
    id_pedido: str
    origem: str
    destino: str
    peso_kg: float = Field(gt=0)
    prazo_dias: int

class IndustryContract(BaseModel):
    id_maquina: str
    temperatura: float
    vibracao_rpm: float
    horas_ativas: float
    data_sensor: date

class TitanicContract(BaseModel):
    PassengerId: int
    Survived: int
    Pclass: int
    Name: str
    Sex: str
    Age: Optional[float] = None
    SibSp: int
    Parch: int
    Ticket: str
    Fare: float
    Cabin: Optional[str] = None
    Embarked: Optional[str] = None

class DataValidator:
    @staticmethod
    def validate_schema(df, schema_class):
        records = df.to_dict(orient="records")
        return [schema_class(**row) for row in records]

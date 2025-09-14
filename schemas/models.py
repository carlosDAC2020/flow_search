# schemas/models.py
from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field

# --- Modelo para la generación de Queries ---
class SearchQuery(BaseModel):
    idea: str = Field(description="La idea o el enfoque principal de la búsqueda.")
    international_query: str = Field(description="Query de búsqueda para oportunidades internacionales (en inglés).")
    national_query: str = Field(description="Query de búsqueda para oportunidades nacionales en Colombia (en español).")

class QueryList(BaseModel):
    queries: List[SearchQuery] = Field(description="Una lista de 5 pares de queries de búsqueda generadas.")


# --- Modelo para el paso de "Identification of Opportunities" (¡A futuro!) ---
class FundingOpportunity(BaseModel):
    origin: str = Field(description="Nombre de la organización o convocatoria que ofrece la financiación.")
    description: str = Field(description="Un resumen conciso de la oportunidad de financiación.")
    financing_type: str = Field(description="Tipo de financiación (ej. grant, inversión de capital, subsidio).")
    main_requirements: List[str] = Field(description="Lista de los requisitos principales para aplicar.")
    application_deadline: str = Field(description="Fecha límite para la postulación (formato YYYY-MM-DD).")
    url: str = Field(description="El enlace directo a la página de la convocatoria.")
# src/pipelines/full_agent.py
import json
import uuid
from typing import List
from langchain_core.runnables import RunnableLambda

from .discovery import create_discovery_pipeline
from .enrichment import create_enrichment_orchestrator as create_enrichment_pipeline
from ..utils.normalizers import flatten_opportunities
from ..schemas.models import FundingOpportunity

# --- ¡NUEVA LÓGICA DE TRANSICIÓN! ---
def persist_and_assign_ids(discovered_opportunities: List[FundingOpportunity]) -> List[dict]:
    """
    Este es el paso intermedio. Simula tres acciones:
    1. Guarda los resultados "crudos" del descubrimiento en un archivo JSON.
    2. Simula la asignación de IDs únicos como lo haría una base de datos.
    3. Devuelve los datos en el formato que espera el pipeline de enriquecimiento (lista de dicts).
    """
    print(f"\n--- [Transition Step] Persisting {len(discovered_opportunities)} discovered opportunities ---\n")
    
    # 1. Guardar el JSON de descubrimiento
    discovery_output_filename = "resultados_descubrimiento.json"
    with open(discovery_output_filename, 'w', encoding='utf-8') as f:
        # Convertimos los objetos Pydantic a dicts para guardarlos
        discovery_dicts = [opp.dict() for opp in discovered_opportunities]
        json.dump(discovery_dicts, f, indent=2, ensure_ascii=False)
    print(f"📄 Resultados preliminares guardados en '{discovery_output_filename}'.")
    
    # 2. Simular la asignación de IDs
    opportunities_with_ids = []
    for opportunity in discovered_opportunities:
        django_id = str(uuid.uuid4())
        print(f"  -> Asignando ID de BD: {django_id} a '{opportunity.origin}'")
        
        opportunity_dict = opportunity.dict()
        opportunity_dict['id'] = django_id
        opportunities_with_ids.append(opportunity_dict)
        
    print("--- Fin del Paso de Transición ---")
    return opportunities_with_ids


def create_full_agent_pipeline():
    """
    Crea y devuelve el pipeline COMPLETO y unificado, incluyendo el paso de
    persistencia y asignación de IDs entre el descubrimiento y el enriquecimiento.
    """
    discovery_pipeline = create_discovery_pipeline().with_config({
        "run_name": "Stage 1: Discovery"
    })
    
    # ¡NUEVO PASO!
    transition_step = RunnableLambda(persist_and_assign_ids).with_config({
        "run_name": "Persisting Discoveries & Assigning IDs"
    })
    
    enrichment_pipeline = create_enrichment_pipeline().with_config({
        "run_name": "Stage 2: Enrichment"
    })

    final_formatter = RunnableLambda(flatten_opportunities).with_config({
        "run_name": "Formatting Final Output"
    })

    # --- PIPELINE UNIFICADO CON EL NUEVO PASO ---
    full_pipeline = (
        discovery_pipeline 
        | transition_step       # <-- ¡Lo insertamos aquí!
        | enrichment_pipeline 
        | final_formatter
    )
    
    return full_pipeline
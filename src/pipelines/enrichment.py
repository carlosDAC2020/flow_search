# src/pipelines/enrichment.py
import time
from typing import List, Dict
from langchain_core.runnables import RunnableLambda
from ..components.enricher import create_full_enrichment_pipeline
from ..schemas.models import FundingOpportunity

def create_enrichment_orchestrator():
    """Crea una cadena que toma una LISTA de oportunidades y las enriquece secuencialmente."""
    
    enrichment_worker_pipeline = create_full_enrichment_pipeline()

    def process_list_sequentially(opportunities_list: List[FundingOpportunity]) -> List[FundingOpportunity]:
        print(f"\n[Enrichment Stage] Iniciando enriquecimiento para {len(opportunities_list)} oportunidades...")
        enriched_opportunities = []
        
        for opportunity_dict in opportunities_list:
            original_id = opportunity_dict.get("id")
            original_type = opportunity_dict.get("type")

            if not original_id:
                print(f"  -> ❌ Saltando oportunidad porque falta ID: {opportunity_dict.get('origin')}")
                continue
            if not original_type:
                print(f"  -> ❌ Saltando oportunidad porque falta TIPO: {opportunity_dict.get('origin')}")
                continue

            print(f"--- Enriqueciendo ID {original_id}: {opportunity_dict.get('origin')} ---")
            try:
                # --- ¡MODIFICACIÓN CLAVE AQUÍ! ---
                # Creamos un nombre dinámico para la ejecución de cada item.
                # El frontend podrá mostrar "Enriqueciendo: Climate Change AI"...
                run_config = {
                    "run_name": f"Enriching Item: {opportunity_dict.get('origin')[:40]}" # Limitamos a 40 chars
                }
                
                # Pasamos la configuración directamente a la llamada .invoke()
                enriched_result = enrichment_worker_pipeline.invoke(
                    opportunity_dict, # El worker espera un dict
                    config={"callbacks": run_config.get("callbacks"), **run_config}
                )

                enriched_result.id = original_id
                enriched_result.type = original_type
                
                enriched_opportunities.append(enriched_result)
            except Exception as e:
                print(f"  -> ❌ Error crítico durante el enriquecimiento: {e}")
                continue
            time.sleep(2)
            
        return enriched_opportunities

    return RunnableLambda(process_list_sequentially)
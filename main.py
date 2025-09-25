# main.py
import json
import argparse # ¡El módulo para crear CLIs!
import os
from langchain_core.output_parsers import JsonOutputParser

# Importamos los constructores de pipelines y funciones necesarias
from src.pipelines.full_agent import create_full_agent_pipeline, persist_and_assign_ids
from src.pipelines.discovery import create_discovery_pipeline
from src.pipelines.enrichment import create_enrichment_orchestrator as create_enrichment_pipeline
from src.schemas.models import QueryList, FundingOpportunity
from src.utils.normalizers import flatten_opportunities

def run_full_agent(initial_input: dict):
    """Ejecuta el pipeline completo de principio a fin."""
    print("🚀 Ejecutando el flujo completo (Descubrimiento -> Persistencia -> Enriquecimiento)...")
    agent_pipeline = create_full_agent_pipeline()
    final_results = agent_pipeline.invoke(initial_input)
    
    output_filename = "resultados_finales_enriquecidos.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, indent=2, ensure_ascii=False)
    print(f"\n📄 Se guardaron {len(final_results)} oportunidades finales y enriquecidas en '{output_filename}'.")

def run_discovery_only(initial_input: dict):
    """Ejecuta solo el pipeline de descubrimiento y guarda el resultado."""
    print("🚀 Ejecutando Fase 1 solamente: Descubrimiento...")
    discovery_pipeline = create_discovery_pipeline()
    discovery_results = discovery_pipeline.invoke(initial_input)
    
    output_filename = "resultados_descubrimiento.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        discovery_dicts = [opp.dict() for opp in discovery_results]
        json.dump(discovery_dicts, f, indent=2, ensure_ascii=False)
    print(f"\n📄 Se guardaron {len(discovery_results)} oportunidades descubiertas en '{output_filename}'.")

def run_enrichment_only(input_filename: str):
    """Ejecuta solo el pipeline de enriquecimiento, cargando desde un archivo JSON."""
    print(f"🚀 Ejecutando Fase 2 solamente: Enriquecimiento desde '{input_filename}'...")
    
    if not os.path.exists(input_filename):
        print(f"❌ Error: El archivo de entrada '{input_filename}' no fue encontrado.")
        return

    with open(input_filename, 'r', encoding='utf-8') as f:
        discovered_data = json.load(f)
        # Convertimos los dicts a objetos Pydantic, que es lo que espera el paso de transición
        discovered_opportunities = [FundingOpportunity(**data) for data in discovered_data]

    # 1. Usamos la función de transición para asignar IDs (no guardará el archivo de nuevo, pero está bien)
    opportunities_to_enrich = persist_and_assign_ids(discovered_opportunities)
    
    # 2. Creamos y ejecutamos el pipeline de enriquecimiento
    enrichment_pipeline = create_enrichment_pipeline()
    enriched_results = enrichment_pipeline.invoke(opportunities_to_enrich)
    
    # 3. Aplanamos y guardamos el resultado final
    final_results_dict = flatten_opportunities(enriched_results)

    output_filename = "resultados_finales_enriquecidos.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(final_results_dict, f, indent=2, ensure_ascii=False)
    print(f"\n📄 Se guardaron {len(final_results_dict)} oportunidades finales y enriquecidas en '{output_filename}'.")


if __name__ == "__main__":
    # --- Configuración del Command-Line Interface (CLI) ---
    parser = argparse.ArgumentParser(description="Agente de Vigilancia de Financiación.")
    parser.add_argument(
        "mode", 
        choices=["full", "discovery-only", "enrich-only"],
        help="El modo de ejecución del agente."
    )
    parser.add_argument(
        "-i", "--input-file",
        default="resultados_descubrimiento.json",
        help="Archivo JSON de entrada para el modo 'enrich-only'."
    )
    
    args = parser.parse_args()
    
    # --- Lógica de Ejecución ---
    print("🤖 Iniciando Agente de Vigilancia de Financiación...")
    
    if args.mode == "enrich-only":
        run_enrichment_only(args.input_file)
    else:
        # Los modos 'full' y 'discovery-only' necesitan la misma entrada inicial
        user_project = {
            "title": "Detección de deforestación con IA",
            "description": "Sistema de detección de deforestación...",
            "keywords": ["deforestación", "cambio climático", "IA"]
        }
        user_input_str = f"Título: {user_project['title']}\nDescripción: {user_project['description']}\nKeywords: {', '.join(user_project['keywords'])}"
        
        parser_obj = JsonOutputParser(pydantic_object=QueryList)
        initial_input = {
            "project_details": user_input_str,
            "format_instructions": parser_obj.get_format_instructions()
        }
        
        if args.mode == "full":
            run_full_agent(initial_input)
        elif args.mode == "discovery-only":
            run_discovery_only(initial_input)
            
    print("\n✅✅✅ Proceso finalizado. ✅✅✅")
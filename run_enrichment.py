
import json
import time
from typing import List, Dict, Any
from langchain_core.runnables import RunnableLambda
from chains.deep_dive_agent import create_full_enrichment_pipeline

def run_enrichment_flow():
    """
    Orquesta el flujo de enriquecimiento de oportunidades.
    """
    # --- PASO 1: OBTENER LOS RESULTADOS DEL PRIMER FLUJO ---
    
    print(" C-Cargando resultados preliminares del flujo de descubrimiento...")
    try:
        with open('resultados_preliminares.json', 'r', encoding='utf-8') as f:
            preliminary_results = json.load(f)
        print(f"-> Se cargaron {len(preliminary_results)} oportunidades para enriquecer.")
    except FileNotFoundError:
        print("-> No se encontró 'resultados_preliminares.json'")

    # --- PASO 2: INICIALIZAR EL AGENTE DE ENRIQUECIMIENTO ---
    print("\n🔗 Construyendo el pipeline de enriquecimiento...")
    enrichment_pipeline = create_full_enrichment_pipeline()

    def process_list_sequentially(opportunities_list: List[Dict]) -> List[Dict]:
        """
        Toma una lista de oportunidades y las procesa una por una,
        llamando a la cadena trabajadora.
        """
        print(f"\n🚀 Iniciando el proceso de enriquecimiento secuencial para {len(opportunities_list)} oportunidades...")
        final_enriched_opportunities = []
        
        for i, opportunity in enumerate(opportunities_list):
            print(f"\n--- Procesando oportunidad {i+1}/{len(opportunities_list)}: {opportunity.get('origin')} ---")
            try:
                # Invocamos la cadena trabajadora para un solo elemento
                enriched_result = enrichment_pipeline.invoke(opportunity)
                
                # Convertimos el objeto Pydantic a un diccionario
                final_enriched_opportunities.append(enriched_result.dict())
                
                print(f"  -> ✅ Enriquecimiento completado.")
                
                # Pausa para respetar los límites de la API
                time.sleep(2)

            except Exception as e:
                print(f"  -> ❌ Error crítico al procesar la oportunidad: {e}")
                continue # Continuamos con la siguiente oportunidad
        
        return final_enriched_opportunities

    # Creamos la cadena orquestadora principal usando RunnableLambda.
    # Esta cadena toma la lista completa como entrada y ejecuta nuestra función de bucle.
    sequential_orchestrator_chain = RunnableLambda(process_list_sequentially)

    # --- PASO 3: EJECUTAR LA CADENA ORQUESTADORA  ---
    
    # Invocamos la cadena orquestadora, pasándole la lista completa.
    final_results = sequential_orchestrator_chain.invoke(preliminary_results)

    # --- PASO 4: GUARDAR Y MOSTRAR RESULTADOS FINALES ---
    print("\n\n✅ Flujo de enriquecimiento completado.")
    
    output_filename = "resultados_enriquecidos.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, indent=2, ensure_ascii=False)
        
    print(f"\n📄 Se guardaron {len(final_results)} oportunidades enriquecidas en '{output_filename}'.")


if __name__ == "__main__":
    run_enrichment_flow()
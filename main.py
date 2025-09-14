# main.py
import json
from typing import List, Dict, Any
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import JsonOutputParser

from chains.query_generator import create_query_generator_chain
from chains.research_agent import create_research_chain
from schemas.models import QueryList
from utils.normalizers import flatten_queries, combine_results


def main():
    """
    Orquesta el flujo completo de vigilancia tecnológica.
    """
    # --- Datos de entrada del proyecto (sin cambios) ---
    user_project = {
        "title": "Detección de deforestación con IA",
        "description": "Sistema de detección de deforestación en áreas rurales con inteligencia artificial para ayudar a los campesinos a tomar medidas de acción y promover la conservación.",
        "keywords": ["deforestación", "cambio climático", "inteligencia artificial", "monitoreo ambiental", "sostenibilidad", "agricultura"]
    }
    user_input_str = f"Título del proyecto: {user_project['title']}\nDescripción: {user_project['description']}\nPalabras clave: {', '.join(user_project['keywords'])}"
    
    # --- Construcción del pipeline completo (Lógica actualizada) ---
    print("\n🔗 Construyendo el pipeline de vigilancia...")
    
    query_generator = create_query_generator_chain()
    researcher = create_research_chain()
    
    # Unimos los componentes con la nueva lógica de aplanamiento
    full_pipeline = (
        query_generator # extracion te queris de busqeda en priemra instancia
        | RunnableLambda(lambda x: x['queries'])  # 1. Extrae la lista de pares de queries
        | RunnableLambda(flatten_queries)        # 2. Aplana la lista en queries individuales
        | researcher.map()                       # 3. Ejecuta la búsqueda para CADA query
        | RunnableLambda(combine_results)        # 4. Combina todas las listas de resultados en una sola
    )

    # --- Ejecución del pipeline (sin cambios) ---
    print("\n🚀 Ejecutando el pipeline completo...")
    
    parser = JsonOutputParser(pydantic_object=QueryList)
    initial_input = {
        "project_details": user_input_str,
        "format_instructions": parser.get_format_instructions()
    }
    
    final_results = full_pipeline.invoke(initial_input)
    
    print("\n✅ Pipeline completado exitosamente.")
    print(f"\n📄 Se encontraron {len(final_results)} resultados en total. Mostrando la lista combinada:\n")
    print(json.dumps(final_results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
# main.py
import json
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import JsonOutputParser

# Importamos las cadenas de los agentes
from chains.query_generator import create_query_generator_chain
from chains.research_agent import create_research_chain
from chains.scrutinizer_agent import create_scrutinizer_chain
from chains.extractor_agent import create_full_extraction_pipeline

# Importamos los modelos Pydantic
from schemas.models import QueryList

# ¡Importamos las NUEVAS funciones secuenciales!
from utils.normalizers import (
    flatten_queries, 
    combine_results, 
    flatten_opportunities,
    scrutinize_sequentially, # <--- NUEVA
    extract_sequentially     # <--- NUEVA
)

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
    
    # --- Construcción del pipeline completo con lógica SECUENCIAL ---
    print("\n🔗 Construyendo el pipeline de vigilancia con pasos secuenciales...")
    
    query_generator = create_query_generator_chain()
    researcher = create_research_chain()
    scrutinizer = create_scrutinizer_chain()
    extractor = create_full_extraction_pipeline()
    
    # Unimos los componentes usando las nuevas funciones
    full_pipeline = (
        query_generator
        | RunnableLambda(lambda x: x['queries'])
        | RunnableLambda(flatten_queries)
        | researcher.map()  # La búsqueda sí puede ser en paralelo, es eficiente
        | RunnableLambda(combine_results)
        # 5. Escrutinio SECUENCIAL
        | RunnableLambda(lambda results: scrutinize_sequentially(results, scrutinizer))
        # 6. Extracción SECUENCIAL
        | RunnableLambda(lambda results: extract_sequentially(results, extractor))
        # 7. Aplanamos la lista final de oportunidades
        | RunnableLambda(flatten_opportunities)
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
    print(f"\n📄 Se encontraron {len(final_results)} oportunidades de financiación. Mostrando la lista final:\n")
    print(json.dumps(final_results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
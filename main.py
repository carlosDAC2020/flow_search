# main.py
import json
from langchain_core.output_parsers import JsonOutputParser

# Importamos el constructor del pipeline completo desde nuestra nueva estructura
from src.pipelines.full_agent import create_full_agent_pipeline
from src.schemas.models import QueryList # Lo necesitamos para el parser

def run_agent():
    """
    Punto de entrada principal para ejecutar el agente de vigilancia de financiación.
    """
    print("🤖 Iniciando Agente de Vigilancia de Financiación...")
    
    # 1. Definir la entrada del proyecto
    user_project = {
        "title": "Detección de deforestación con IA",
        "description": "Sistema de detección de deforestación en áreas rurales...",
        "keywords": ["deforestación", "cambio climático", "inteligencia artificial"]
    }
    user_input_str = f"Título del proyecto: {user_project['title']}\nDescripción: {user_project['description']}\nPalabras clave: {', '.join(user_project['keywords'])}"
    
    parser = JsonOutputParser(pydantic_object=QueryList)
    initial_input = {
        "project_details": user_input_str,
        "format_instructions": parser.get_format_instructions()
    }
    
    # 2. Crear el pipeline completo
    print("🔗 Construyendo el pipeline completo del agente...")
    agent_pipeline = create_full_agent_pipeline()
    
    # 3. Invocar el pipeline una sola vez
    print("\n🚀 Ejecutando el flujo completo (Descubrimiento -> Enriquecimiento)...")
    final_results = agent_pipeline.invoke(initial_input)
    
    # 4. Mostrar el resultado final
    print("\n\n✅✅✅ AGENTE COMPLETADO EXITOSAMENTE ✅✅✅")
    
    """
    output_filename = "resultados_finales_enriquecidos.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        # La salida ya son dicts por el `flatten_opportunities`, así que está listo para json.dump
        json.dump(final_results, f, indent=2, ensure_ascii=False)
        
    print(f"\n📄 Se guardaron {len(final_results)} oportunidades finales y enriquecidas en '{output_filename}'.")
    """
    
if __name__ == "__main__":
    run_agent()
import os
import json
from dotenv import load_dotenv
from typing import List, Dict, Any

# --- Componentes de LangChain ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
# --- Herramientas de Búsqueda ---
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import BraveSearch

# --- Cargar variables de entorno desde .env ---
load_dotenv()
print("🔑 Variables de entorno cargadas.")


# pip install -U langgraph "langchain[openai]"

# --------------------------------------------------------------------------
# PARTE 1: DEFINICIONES DE ESTRUCTURA Y MODELO (Sin cambios)
# --------------------------------------------------------------------------
class SearchQuery(BaseModel):
    idea: str = Field(description="La idea o el enfoque principal de la búsqueda.")
    international_query: str = Field(description="Query de búsqueda para oportunidades internacionales (en inglés).")
    national_query: str = Field(description="Query de búsqueda para oportunidades nacionales en Colombia (en español).")

class QueryList(BaseModel):
    queries: List[SearchQuery] = Field(description="Una lista de 5 pares de queries de búsqueda generadas.")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.2
)

# --------------------------------------------------------------------------
# PARTE 2: GENERACIÓN DE QUERIES (Sin cambios)
# --------------------------------------------------------------------------
system_prompt = """
Actúa como un experto en la búsqueda de financiación para proyectos de innovación y tecnología. 
Tu tarea es generar consultas de búsqueda (queries) estratégicas para encontrar oportunidades de financiación (grants, funding, convocatorias, etc.) basadas en la descripción de un proyecto que te proporcionará el usuario.
Debes analizar el título, la descripción y las palabras clave del proyecto para crear 5 ideas de búsqueda diferentes y efectivas.
Por cada idea, genera dos versiones de la query:
1.  Una para búsquedas internacionales, en inglés.
2.  Una para búsquedas a nivel nacional (Colombia), en español.
Utiliza sinónimos y términos relacionados como "funding", "grants", "convocatorias", "financiación", "proyectos de investigación", "venture capital for green tech", etc.
{format_instructions}
"""
user_project = {
    "title": "Detección de deforestación con IA",
    "description": "Sistema de detección de deforestación en áreas rurales con inteligencia artificial para ayudar a los campesinos a tomar medidas de acción y promover la conservación.",
    "keywords": ["deforestación", "cambio climático", "inteligencia artificial", "monitoreo ambiental", "sostenibilidad", "agricultura"]
}
user_input_str = f"Título del proyecto: {user_project['title']}\nDescripción: {user_project['description']}\nPalabras clave: {', '.join(user_project['keywords'])}"

parser = JsonOutputParser(pydantic_object=QueryList)
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{project_details}"),
])
query_generation_chain = prompt_template | llm | parser

print("\n🤖 Generando queries de búsqueda...")
generated_queries = query_generation_chain.invoke({
    "project_details": user_input_str,
    "format_instructions": parser.get_format_instructions()
})
print("\n✅ Queries generadas exitosamente.")

# --------------------------------------------------------------------------
# PARTE 3: FLUJO DE EJECUCIÓN UNIFICADO CON LCEL (REEMPLAZA LAS PARTES 3 Y 4)
# --------------------------------------------------------------------------
print("\n🔎 Definiendo el flujo de búsqueda y normalización con LCEL...")

# -- Creamos nuestra acción de fallback: una función que siempre devuelve una lista vacía --
# Usamos un RunnableLambda para poder insertarla en nuestra cadena.
fallback_to_empty_list = RunnableLambda(lambda x: [])

# 1. Inicializamos las herramientas de búsqueda 
tavily_tool = TavilySearchResults(
        max_results=3
    ).with_retry(
        stop_after_attempt=3,
        wait_exponential_jitter=True
    ).with_fallbacks(
        fallbacks=[fallback_to_empty_list] # Si los reintentos fallan, devuelve []
    )

brave_tool = BraveSearch.from_api_key(
        api_key=os.getenv("BRAVE_SEARCH_API_KEY"), 
        search_kwargs={"count": 3}
    ).with_retry(
        stop_after_attempt=3,
        wait_exponential_jitter=True
    ).with_fallbacks(
        fallbacks=[fallback_to_empty_list] # Si los reintentos fallan, devuelve []
    )


# 2. Creamos el Runnable paralelo para una sola búsqueda
parallel_search_step = RunnableParallel(
    tavily=tavily_tool,
    brave=brave_tool
)

# 3. Creamos la función y el RunnableLambda para la normalización
def normalize_results(raw_results: Dict[str, Any]) -> List[Dict[str, str]]:
    normalized = []
    # (La lógica de esta función es idéntica a la anterior)
    for res in raw_results.get("tavily", []):
        normalized.append({
            "title": res.get("title", "Sin título"), "url": res.get("url"), "description": res.get("content")
        })
    brave_res_list = raw_results.get("brave", [])
    if isinstance(brave_res_list, str):
        try: brave_res_list = json.loads(brave_res_list)
        except json.JSONDecodeError: brave_res_list = []
    for res in brave_res_list:
        normalized.append({
            "title": res.get("title", "Sin título"), "url": res.get("link"), "description": res.get("snippet")
        })
    return normalized

normalization_step = RunnableLambda(normalize_results)

# 4. Creamos la cadena que procesa UNA SOLA idea de búsqueda
# Toma una query, la busca en paralelo y normaliza el resultado.
search_and_normalize_chain = parallel_search_step | normalization_step

# 5. Creamos la cadena que procesa un par de queries (nacional e internacional)
# Usa RunnableParallel para ejecutar la cadena anterior en ambas queries al mismo tiempo.
process_query_pair_chain = RunnableParallel(
    international_search=RunnableLambda(lambda x: {"query": x['international_query']}) | search_and_normalize_chain,
    national_search=RunnableLambda(lambda x: {"query": x['national_query']}) | search_and_normalize_chain,
    # Pasamos la 'idea' original para que no se pierda
    idea=RunnableLambda(lambda x: x['idea'])
)

# 6. ¡LA MAGIA! Creamos la cadena completa que une todo
#    - Primero genera las queries.
#    - Luego extrae la lista de 'queries' del resultado.
#    - Finalmente, usa .map() para aplicar `process_query_pair_chain` a CADA elemento de la lista.
full_pipeline = query_generation_chain | RunnableLambda(lambda x: x['queries']) | process_query_pair_chain.map()

# --------------------------------------------------------------------------
# PARTE 4: INVOCACIÓN Y VISUALIZACIÓN
# --------------------------------------------------------------------------
print("\n🚀 Ejecutando el pipeline completo...")

# El input inicial es el mismo que antes
initial_input = {
    "project_details": user_input_str,
    "format_instructions": parser.get_format_instructions()
}

# Invocamos la cadena completa UNA SOLA VEZ
final_results = full_pipeline.invoke(
    initial_input
)

print("\n✅ Pipeline completado.")

# Imprimimos los resultados finales
print("\n📄 Resultados finales y normalizados:\n")
print(json.dumps(final_results, indent=2, ensure_ascii=False))
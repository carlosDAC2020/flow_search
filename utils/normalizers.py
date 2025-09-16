# utils/normalizers.py
import json
import time
from typing import List, Dict, Any
from langchain_core.runnables import Runnable
from schemas.models import FundingOpportunityList

# --- Funciones que no cambian ---
def flatten_queries(query_list: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    flat_list = []
    for item in query_list:
        if item.get('international_query'):
            flat_list.append({"query": item['international_query']})
        if item.get('national_query'):
            flat_list.append({"query": item['national_query']})
    return flat_list

def combine_results(list_of_lists: List[List[Dict]]) -> List[Dict]:
    combined = []
    for sublist in list_of_lists:
        # Pequeña validación para evitar errores si un sublist no es una lista
        if isinstance(sublist, list):
            combined.extend(sublist)
    return combined

def normalize_search_results(raw_results: Dict[str, Any]) -> List[Dict[str, str]]:
    normalized = []
    for res in raw_results.get("tavily", []):
        normalized.append({
            "title": res.get("title", "Sin título"),
            "url": res.get("url"),
            "description": res.get("content")
        })
    brave_res_list = raw_results.get("brave", [])
    if isinstance(brave_res_list, str):
        try: brave_res_list = json.loads(brave_res_list)
        except json.JSONDecodeError: brave_res_list = []
    for res in brave_res_list:
        normalized.append({
            "title": res.get("title", "Sin título"),
            "url": res.get("link"),
            "description": res.get("snippet")
        })
    return normalized

def flatten_opportunities(list_of_opportunity_lists: List[FundingOpportunityList]) -> List[dict]:
    final_list = []
    for opportunity_list in list_of_opportunity_lists:
        # Nos aseguramos de que el objeto es del tipo esperado antes de acceder a sus atributos
        if isinstance(opportunity_list, FundingOpportunityList):
            for opportunity in opportunity_list.opportunities:
                final_list.append(opportunity.dict())
    return final_list

# --- ¡NUEVA FUNCIÓN SECUENCIAL PARA EL ESCRUTINIO! ---
def scrutinize_sequentially(search_results: List[Dict], scrutinizer_chain: Runnable) -> List[Dict]:
    """
    Toma una lista de resultados, los evalúa UNO A UNO con el agente de escrutinio,
    y devuelve solo los que son considerados relevantes.
    """
    if not search_results:
        return []

    print(f"\n🔎 Realizando escrutinio secuencial para {len(search_results)} resultados...")
    
    filtered_results = []
    for result in search_results:
        try:
            print(f"  -> Escrutando: {result.get('title', 'Sin título')}")
            # Usamos .invoke() para procesar un único elemento a la vez.
            scrutiny_output = scrutinizer_chain.invoke(result)
            
            if scrutiny_output.is_relevant:
                print(f"    ✅ Relevante.")
                filtered_results.append(result)
            else:
                print(f"    ❌ Descartado.")
            
            # Pausa opcional para ser extra cuidadoso con el rate limit.
            # 1 segundo de pausa significa que no harás más de 60 peticiones por minuto.
            time.sleep(1)

        except Exception as e:
            print(f"    ⚠️ Error durante el escrutinio de {result.get('url')}: {e}")
            continue # Continuamos con el siguiente resultado

    print(f"\n✅ Escrutinio completado. {len(filtered_results)} fuentes relevantes pasarán a la extracción.")
    return filtered_results

# --- ¡NUEVA FUNCIÓN SECUENCIAL PARA LA EXTRACCIÓN! ---
def extract_sequentially(relevant_results: List[Dict], extractor_chain: Runnable) -> List[FundingOpportunityList]:
    """
    Toma una lista de resultados relevantes y ejecuta el pipeline de extracción
    (scraping + LLM) de forma secuencial para cada uno.
    """
    if not relevant_results:
        return []
    
    print(f"\n⛏️  Extrayendo información de {len(relevant_results)} fuentes de forma secuencial...")
    
    all_opportunities = []
    for result in relevant_results:
        try:
            print(f"  -> Extrayendo de: {result.get('url')}")
            # Invocamos la cadena de extracción completa para un solo resultado.
            # Esta cadena ya incluye el paso de scraping.
            opportunity_list = extractor_chain.invoke(result)
            all_opportunities.append(opportunity_list)

            # Pausa opcional para el modelo más caro/lento (gemini-1.5-pro)
            time.sleep(2) 

        except Exception as e:
            print(f"    ⚠️ Error durante la extracción de {result.get('url')}: {e}")
            continue

    return all_opportunities
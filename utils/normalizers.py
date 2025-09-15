import json
from typing import List, Dict, Any
from langchain_core.runnables import Runnable
from schemas.models import FundingOpportunityList

def flatten_queries(query_list: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Toma la lista de diccionarios de queries generadas y la aplana en una 
    lista simple de queries individuales, listas para ser procesadas por .map().
    Entrada: [{'idea': ..., 'international_query': 'q1', 'national_query': 'q2'}, ...]
    Salida: [{'query': 'q1'}, {'query': 'q2'}, ...]
    """
    flat_list = []
    for item in query_list:
        if item.get('international_query'):
            flat_list.append({"query": item['international_query']})
        if item.get('national_query'):
            flat_list.append({"query": item['national_query']})
    return flat_list

def combine_results(list_of_lists: List[List[Dict]]) -> List[Dict]:
    """
    Toma una lista de listas de resultados y la aplana en una única lista.
    Entrada: [[res1, res2], [res3], [res4, res5, res6]]
    Salida: [res1, res2, res3, res4, res5, res6]
    """
    combined = []
    for sublist in list_of_lists:
        combined.extend(sublist)
    return combined

def normalize_search_results(raw_results: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Toma los resultados brutos de Tavily y Brave y los convierte a un formato estándar.
    """
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
    """
    Toma una lista de objetos FundingOpportunityList y la aplana en una
    única lista de diccionarios de oportunidades.
    """
    final_list = []
    for opportunity_list in list_of_opportunity_lists:
        for opportunity in opportunity_list.opportunities:
            final_list.append(opportunity.dict()) # Convertimos a dict para el JSON final
    return final_list

def filter_results_with_scrutinizer(search_results: List[Dict], scrutinizer_chain: Runnable):
    """
    Toma una lista de resultados de búsqueda, los evalúa con el agente de escrutinio,
    y devuelve solo los que son considerados relevantes.
    """
    if not search_results:
        return []

    print(f"🔎 Se encontraron {len(search_results)} resultados únicos. Realizando escrutinio...")
    
    # Usamos .batch() para evaluar todos los resultados en paralelo, ¡muy eficiente!
    scrutiny_outputs = scrutinizer_chain.batch(search_results)
    
    filtered_results = []
    for original_result, scrutiny_result in zip(search_results, scrutiny_outputs):
        if scrutiny_result.is_relevant:
            print(f"  -> ✅ Relevante: {original_result['title']}")
            filtered_results.append(original_result)
        else:
            print(f"  -> ❌ Descartado: {original_result['title']} (Razón: {scrutiny_result.reason})")

    print(f"✅ Escrutinio completado. {len(filtered_results)} fuentes relevantes pasarán a la extracción.")
    return filtered_results
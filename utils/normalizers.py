import json
from typing import List, Dict, Any


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
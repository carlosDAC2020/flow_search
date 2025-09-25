# utils/normalizers.py
import json
import time
from typing import List, Dict, Any
from langchain_core.runnables import Runnable
from ..schemas.models import FundingOpportunityList
from pydantic import BaseModel      # <-- ¡Importante añadir esta importación!

# --- Funciones que no cambian ---
def flatten_queries(query_list: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    flat_list = []
    for item in query_list:
        if item.get('international_query'):
            flat_list.append({"query": item['international_query'], "type": "International"})
        if item.get('national_query'):
            flat_list.append({"query": item['national_query'], "type": "National"})
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

def flatten_opportunities(list_of_items: List[Any]) -> List[dict]:
    """
    Toma una lista que puede contener objetos Pydantic FundingOpportunity O diccionarios
    y la convierte de forma robusta en una única lista de diccionarios.
    """
    final_list = []
    if not list_of_items:
        return final_list
        
    for item in list_of_items:
        # Si el item es cualquier tipo de modelo Pydantic, lo convertimos a dict.
        if isinstance(item, BaseModel):
            final_list.append(item.dict())
        # Si ya es un diccionario, simplemente lo añadimos.
        elif isinstance(item, dict):
            final_list.append(item)
            
    return final_list
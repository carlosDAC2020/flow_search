# chains/research_agent.py
from langchain_core.runnables import RunnableParallel, RunnableLambda
from langchain_community.tools.tavily_search import TavilySearchResults
"""
usar el tavili de langchain 
from langchain_tavily import TavilySearch
"""
from langchain_community.tools import BraveSearch

from config import settings
from utils.normalizers import normalize_search_results

def create_research_chain():
    """Construye y devuelve la cadena que busca en paralelo y normaliza los resultados."""
    
    fallback_to_empty_list = RunnableLambda(lambda x: [])

    tavily_tool = TavilySearchResults(
        max_results=settings.TAVILY_MAX_RESULTS
    ).with_retry(stop_after_attempt=3, wait_exponential_jitter=True).with_fallbacks([fallback_to_empty_list])

    brave_tool = BraveSearch.from_api_key(
        api_key=settings.BRAVE_SEARCH_API_KEY, 
        search_kwargs={"count": settings.BRAVE_SEARCH_COUNT}
    ).with_retry(stop_after_attempt=3, wait_exponential_jitter=True).with_fallbacks([fallback_to_empty_list])

    parallel_search_step = RunnableParallel(tavily=tavily_tool, brave=brave_tool)
    
    normalization_step = RunnableLambda(normalize_search_results)
    
    search_and_normalize_chain = parallel_search_step | normalization_step
    
    # Devolvemos la cadena que procesa un par de queries, para ser usada con .map() en main.py
    return search_and_normalize_chain
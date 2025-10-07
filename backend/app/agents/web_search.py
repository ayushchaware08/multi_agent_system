import os, time
from app.utils.backoff_utils import with_retry
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_groq.chat_models import ChatGroq

@with_retry(max_tries=3, exceptions=(Exception,), delay=2)
def run_web_search(query):
    """
    Web search using DuckDuckGo only.
    Flow: controller.py → web_search.py → DuckDuckGo → ChatGroq LLM → user
    """
    try:
        # Use DuckDuckGo for web search (no API key required)
        search_tool = DuckDuckGoSearchResults(num_results=5)
        search_results = search_tool.run(query)
        
        # Ensure we have GROQ_API_KEY for LLM summarization
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key:
            raise RuntimeError("GROQ_API_KEY is required for web search summarization; set GROQ_API_KEY in environment")
        
        # Summarize results with ChatGroq LLM
        llm = ChatGroq(api_key=groq_key, temperature=0.1)
        
        prompt = f"""Based on the following web search results for "{query}", provide a comprehensive answer.
            Search Results:
            {search_results}

            Please provide:
            1. A clear, concise answer to the query
            2. Key points from the search results
            3. 2-3 relevant source references

            Format your response in a user-friendly way."""

        start_time = time.time()
        summary = llm.invoke(prompt).content
        duration = time.time() - start_time
        
        # Build trace for debugging/logging
        trace = {
            "search_engine": "DuckDuckGo", 
            "raw_results": str(search_results)[:1000],  # truncate for storage
            "llm_duration": duration,
            "query": query
        }
        
        return summary, trace
        
    except Exception as e:
        error_msg = f"Web search failed: {str(e)}"
        trace = {"error": str(e), "search_engine": "DuckDuckGo"}
        return error_msg, trace

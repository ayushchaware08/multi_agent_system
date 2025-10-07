import os
import logging
from langchain_groq import ChatGroq
from serpapi import GoogleSearch

logger = logging.getLogger(__name__)

GROQ_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")

def run_web_search(query):
    """
    Run web search using SerpAPI (Google) and generate comprehensive answer with LLM
    """
    try:
        logger.info(f"🔍 Web search query: '{query}'")
        
        # Check if SerpAPI key is available
        if not SERPAPI_KEY:
            logger.error("❌ SERPAPI_API_KEY not found in environment")
            return (
                "SerpAPI key not configured. Please add SERPAPI_API_KEY to your .env file.",
                {"error": "SERPAPI_API_KEY not found", "search_engine": "SerpAPI"}
            )
        
        # Perform Google search via SerpAPI
        logger.info("📡 Searching via SerpAPI (Google)...")
        params = {
            "q": query,
            "api_key": SERPAPI_KEY,
            "num": 5,
            "engine": "google",
            "google_domain": "google.com",
            "gl": "us",
            "hl": "en"
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Extract organic results
        organic_results = results.get("organic_results", [])
        
        if not organic_results:
            logger.warning("⚠️ No search results found")
            return (
                "No search results found for this query. Please try rephrasing your question.",
                {
                    "search_engine": "SerpAPI (Google)",
                    "results_count": 0,
                    "query": query
                }
            )
        
        logger.info(f"✅ Found {len(organic_results)} results")
        
        # Format search results for LLM context
        formatted_results = "\n\n".join([
            f"[Source {i+1}]\n"
            f"Title: {result.get('title', 'N/A')}\n"
            f"URL: {result.get('link', 'N/A')}\n"
            f"Content: {result.get('snippet', 'N/A')}"
            for i, result in enumerate(organic_results[:5])
        ])
        
        # Initialize Groq LLM
        llm = ChatGroq(
            api_key=GROQ_KEY,
            model="llama-3.3-70b-versatile",
            temperature=0.3,  # Slightly higher for more natural responses
            max_tokens=2048,
            timeout=60.0,
            max_retries=2
        )
        
        # Create comprehensive prompt for LLM
        prompt = f"""You are a helpful AI assistant providing comprehensive, accurate answers based on current web search results.

            User Query: {query}

            Search Results from Google:
            {formatted_results}

            Instructions:
            1. Provide a comprehensive, well-structured answer to the user's query
            2. Synthesize information from multiple sources
            3. Include specific details, dates, facts, and figures when available
            4. Organize information with clear sections using markdown headers (##, ###)
            5. Use bullet points for lists and key information
            6. Mention source titles when referencing specific information
            7. If the query asks for "latest" or "recent" information, prioritize the most current details
            8. Be factual and objective

            Provide your detailed answer:"""
                    
        logger.info("🤖 Generating comprehensive answer with LLM...")
        response = llm.invoke(prompt)
        answer = response.content if hasattr(response, "content") else str(response)
        logger.info("✅ Answer generated successfully")
        
        # Build detailed trace for debugging and transparency
        trace = {
            "search_engine": "SerpAPI (Google)",
            "query": query,
            "results_count": len(organic_results),
            "sources": [
                {
                    "position": i + 1,
                    "title": r.get("title", "N/A"),
                    "link": r.get("link", "N/A"),
                    "snippet": r.get("snippet", "N/A")[:300] + "..." if len(r.get("snippet", "")) > 300 else r.get("snippet", "N/A"),
                    "displayed_link": r.get("displayed_link", "N/A")
                }
                for i, r in enumerate(organic_results[:5])
            ]
        }
        
        return answer, trace
        
    except Exception as e:
        logger.error(f"❌ Web search failed: {str(e)}")
        error_msg = f"Web search failed: {str(e)}"
        trace = {
            "error": str(e),
            "search_engine": "SerpAPI",
            "query": query
        }
        return error_msg, trace

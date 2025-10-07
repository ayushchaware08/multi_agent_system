import os
import time
import logging
from datetime import datetime, timedelta
from app.utils.backoff_utils import with_retry
from langchain_groq.chat_models import ChatGroq
import arxiv

logger = logging.getLogger(__name__)

GROQ_KEY = os.getenv("GROQ_API_KEY")

@with_retry(max_tries=3, exceptions=(Exception,), delay=2)
def run_arxiv_query(query, max_results=8):
    """
    Search arXiv for recent papers on the given topic with enhanced relevance filtering.
    Flow: controller.py → arxiv_agent.py → arXiv API → ChatGroq LLM → user
    """
    try:
        logger.info(f"🔍 ArXiv search query: '{query}'")
        
        # Clean query for better ArXiv search
        clean_query = query.lower()
        for prefix in ["recent papers on", "papers about", "papers on", "find papers", "search for", "research on"]:
            clean_query = clean_query.replace(prefix, "").strip()
        
        # Add field-specific search for better relevance
        # ArXiv supports: ti: (title), abs: (abstract), au: (author), cat: (category)
        if "AI safety" in query or "ai safety" in query.lower():
            search_query = "cat:cs.AI AND (safety OR alignment OR robustness OR interpretability)"
        elif "transformer" in clean_query.lower():
            search_query = "cat:cs.AI AND (transformer OR attention mechanism)"
        elif "reinforcement learning" in clean_query.lower():
            search_query = "cat:cs.LG AND (reinforcement learning OR RL)"
        else:
            search_query = clean_query
        
        logger.info(f"📝 Search query: '{search_query}'")
        
        # Search arXiv with optimized parameters
        search = arxiv.Search(
            query=search_query,
            max_results=max_results * 2,  # Fetch more to filter later
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        
        logger.info("📡 Searching ArXiv...")
        results = list(search.results())
        
        if not results:
            logger.warning("⚠️ No papers found")
            return (
                f"No recent papers found on ArXiv for '{query}'. Try different or broader search terms.",
                {"papers": [], "query": query, "cleaned_query": clean_query}
            )
        
        logger.info(f"✅ Found {len(results)} papers")
        
        # Filter for papers published in last 18 months for "recent" queries
        if "recent" in query.lower() or "latest" in query.lower():
            cutoff_date = datetime.now() - timedelta(days=540)  # 18 months
            results = [r for r in results if r.published.replace(tzinfo=None) > cutoff_date]
            logger.info(f"📅 Filtered to {len(results)} papers from last 18 months")
        
        # Select top papers
        top_papers = results[:max_results]
        
        papers = []
        for r in top_papers:
            submitted_date = r.published.strftime("%Y-%m-%d") if r.published else "Unknown"
            
            papers.append({
                "title": r.title.strip(),
                "summary": r.summary[:600].strip(),  # Balanced length
                "authors": [a.name for a in r.authors],
                "url": r.entry_id,
                "pdf_url": r.pdf_url,
                "published": submitted_date,
                "categories": r.categories,
                "arxiv_id": r.entry_id.split('/')[-1]
            })
        
        if not papers:
            return (
                f"No papers found matching '{query}'. Try broader search terms.",
                {"papers": [], "query": query}
            )
        
        # Ensure GROQ_API_KEY is available
        if not GROQ_KEY:
            raise RuntimeError("GROQ_API_KEY is required; set in environment")
        
        # Use ChatGroq for comprehensive analysis
        llm = ChatGroq(
            api_key=GROQ_KEY,
            model="llama-3.3-70b-versatile",
            temperature=0.3,  # Slightly higher for more natural analysis
            max_tokens=3000,  # Increased for detailed analysis
            timeout=60.0,
            max_retries=2
        )
        
        # Create structured context for LLM
        papers_text = "\n\n".join([
            f"[Paper {i+1}]\n"
            f"Title: {p['title']}\n"
            f"Authors: {', '.join(p['authors'][:5])}{'...' if len(p['authors']) > 5 else ''}\n"
            f"Published: {p['published']}\n"
            f"ArXiv ID: {p['arxiv_id']}\n"
            f"Categories: {', '.join(p['categories'][:3])}\n"
            f"Abstract: {p['summary']}\n"
            f"PDF: {p['pdf_url']}"
            for i, p in enumerate(papers)
        ])
        
        # Enhanced prompt for better structured output
        prompt = f"""You are an AI research assistant analyzing recent academic papers from ArXiv.

            User Query: {query}

            ArXiv Papers Found ({len(papers)} papers):
            {papers_text}

            Please provide a comprehensive, well-structured analysis with the following sections:

            ## Overview
            Provide a 2-3 sentence summary of the current research landscape in this area based on these papers.

            ## Key Papers & Contributions
            For each significant paper (top 3-5), provide:
            - **Paper Title** (in bold)
            - **Key Contribution**: What's the main innovation or finding?
            - **Methodology**: Brief description of approach
            - **Authors & Institution**: Highlight notable researchers
            - **ArXiv ID**: For easy reference

            ## Research Trends & Themes
            Identify common patterns, methodologies, or emerging directions across these papers.

            ## Notable Researchers
            List prominent authors who appear across multiple papers or are from well-known institutions.

            ## Recommended Reading Order
            Suggest which papers to read first and why, based on:
            - Foundational concepts
            - Novelty and impact
            - Recency

            ## Access Links
            Provide direct ArXiv links to the most relevant papers.

            Format Guidelines:
            - Use markdown headers (##, ###)
            - Use **bold** for paper titles and key terms
            - Use bullet points for lists
            - Include ArXiv IDs in format: [2510.05102]
            - Keep the analysis comprehensive but concise

            Provide your detailed analysis:"""
        
        logger.info("🤖 Generating comprehensive analysis...")
        start_time = time.time()
        response = llm.invoke(prompt)
        summary = response.content if hasattr(response, "content") else str(response)
        duration = time.time() - start_time
        logger.info(f"✅ Analysis completed in {duration:.2f}s")
        
        # Build comprehensive trace
        trace = {
            "papers": papers,
            "query": query,
            "cleaned_query": clean_query,
            "search_query": search_query,
            "total_found": len(papers),
            "llm_duration": duration,
            "sort_order": "most_recent_first",
            "date_range": f"Last 18 months" if "recent" in query.lower() else "All time"
        }
        
        return summary, trace
        
    except Exception as e:
        logger.error(f"❌ ArXiv search failed: {str(e)}")
        error_msg = f"ArXiv search failed: {str(e)}"
        trace = {"error": str(e), "query": query}
        return error_msg, trace

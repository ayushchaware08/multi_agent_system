import os, time
from app.utils.backoff_utils import with_retry

from langchain_groq.chat_models import ChatGroq

# from langchain.chat_models import ChatGroq, ChatOpenAI
import arxiv  # pip install arxiv

@with_retry(max_tries=3, exceptions=(Exception,), delay=2)
def run_arxiv_query(query, max_results=5):
    """
    Search arXiv for recent papers on the given topic.
    Flow: controller.py → arxiv_agent.py → arXiv API → ChatGroq LLM → user
    """
    try:
        # Search arXiv, sorted by most recent submission date
        search = arxiv.Search(
            query=query, 
            max_results=max_results, 
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        papers = []
        for r in search.results():
            # Format submission date for better readability
            submitted_date = r.published.strftime("%Y-%m-%d") if r.published else "Unknown"
            
            papers.append({
                "title": r.title.strip(),
                "summary": r.summary[:800],  # Truncate summary for better processing
                "authors": [a.name for a in r.authors],
                "url": r.entry_id,
                "published": submitted_date,
                "categories": r.categories
            })
        
        if not papers:
            return f"No recent papers found for query: '{query}'. Try different keywords.", {"papers": []}
        
        # Ensure GROQ_API_KEY is available
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key:
            raise RuntimeError("GROQ_API_KEY is required for arxiv summarization; set GROQ_API_KEY in environment")
        
        # Use ChatGroq to summarize the papers
        llm = ChatGroq(api_key=groq_key, temperature=0.1)
        
        # Create structured prompt for better LLM response
        papers_text = "\n\n".join([
            f"**{i+1}. {p['title']}**\n"
            f"Authors: {', '.join(p['authors'][:3])}{'...' if len(p['authors']) > 3 else ''}\n"
            f"Published: {p['published']}\n"
            f"Categories: {', '.join(p['categories'][:2])}\n"
            f"Summary: {p['summary']}\n"
            f"URL: {p['url']}"
            for i, p in enumerate(papers)
        ])
        
        prompt = f"""Based on these recent arXiv papers about "{query}", provide a comprehensive summary:

{papers_text}

Please provide:
1. A brief overview of the current research trends in this area
2. Key findings and methodologies from these papers
3. Notable authors or institutions
4. Links to the most relevant papers

Format your response to be informative and accessible."""

        start_time = time.time()
        summary = llm.invoke(prompt).content
        duration = time.time() - start_time
        
        # Build comprehensive trace
        trace = {
            "papers": papers,
            "query": query,
            "total_found": len(papers),
            "llm_duration": duration,
            "sort_order": "most_recent_first"
        }
        
        return summary, trace
        
    except Exception as e:
        error_msg = f"arXiv search failed: {str(e)}"
        trace = {"error": str(e), "query": query}
        return error_msg, trace

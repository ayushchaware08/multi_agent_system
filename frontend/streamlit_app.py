import streamlit as st
import requests
import os

API_ROOT = os.getenv("API_ROOT", "http://localhost:8000")

st.title("Multi-Agent Search / RAG demo")

st.sidebar.header("Upload PDF (NebulaByte demo)")
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])
if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
    try:
        resp = requests.post(f"{API_ROOT}/upload/", files=files)
        resp.raise_for_status()
        try:
            body = resp.json()
            st.sidebar.success("Uploaded: " + str(body))
        except ValueError:
            st.sidebar.success("Uploaded (non-JSON response): " + resp.text)
    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"Upload failed: {e}")

query = st.text_input("Enter your question or search (or type 'recent papers on ...')", "")
if st.button("Ask"):
    payload = {"text": query}
    try:
        r = requests.post(f"{API_ROOT}/ask/", json=payload)
        r.raise_for_status()
        try:
            data = r.json()
        except ValueError:
            st.error("Backend returned non-JSON response: " + r.text)
            data = {}
            # Show a loading spinner while waiting for the response
            with st.spinner("Searching..."):
                pass  # The request has already completed at this point

            # Show search suggestions inside the search box
        suggestions = [
            "recent papers on AI safety",
            "summarize the uploaded PDF",
            "find papers about reinforcement learning",
            "who are the top authors in NLP?",
            "what are the latest trends in computer vision?"
        ]
        if not query:
            st.info("Suggestions: " + ", ".join(suggestions))
        st.subheader("Answer")
        st.write(data.get("answer"))
        st.subheader("Agents used & rationale")
        st.write(data.get("agents_used"))
        st.write(data.get("rationale"))
        if data.get("trace"):
            st.subheader("Trace / retrieved docs")
            st.write(data.get("trace"))
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")

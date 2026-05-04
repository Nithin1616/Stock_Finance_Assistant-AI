import os
import pickle
import faiss
import numpy as np
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
import PyPDF2
import io

# Initialize embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def load_embedding_model():
    """Load sentence transformer model."""
    return SentenceTransformer(EMBEDDING_MODEL)


def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from uploaded PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    """Split text into chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "!", "?", ",", " "],
    )
    chunks = splitter.split_text(text)
    return [chunk.strip() for chunk in chunks if len(chunk.strip()) > 50]


def create_faiss_index(chunks: List[str], model: SentenceTransformer) -> Tuple:
    """Create FAISS index from text chunks."""
    embeddings = model.encode(chunks, show_progress_bar=False)
    embeddings = np.array(embeddings).astype("float32")

    # Normalize for cosine similarity
    faiss.normalize_L2(embeddings)

    # Create index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Inner product = cosine similarity after normalization
    index.add(embeddings)

    return index, chunks, embeddings


def retrieve_relevant_chunks(
    query: str,
    index,
    chunks: List[str],
    model: SentenceTransformer,
    top_k: int = 5
) -> List[str]:
    """Retrieve most relevant chunks for a query."""
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")
    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(query_embedding, top_k)

    relevant_chunks = []
    for i, idx in enumerate(indices[0]):
        if idx != -1 and scores[0][i] > 0.3:  # Similarity threshold
            relevant_chunks.append(chunks[idx])

    return relevant_chunks


def build_rag_context(
    query: str,
    news_articles: list,
    stock_context: str,
    pdf_index=None,
    pdf_chunks: List[str] = None,
    model: SentenceTransformer = None,
) -> str:
    """Build complete RAG context from all sources."""
    context_parts = []

    # 1. Stock data context (always included)
    if stock_context:
        context_parts.append(stock_context)

    # 2. News context (always included if available)
    if news_articles:
        from news_fetcher import format_news_for_llm
        news_context = format_news_for_llm(news_articles)
        context_parts.append(news_context)

    # 3. PDF context (if PDF was uploaded and indexed)
    if pdf_index is not None and pdf_chunks and model:
        relevant_chunks = retrieve_relevant_chunks(query, pdf_index, pdf_chunks, model, top_k=4)
        if relevant_chunks:
            pdf_context = "ANNUAL REPORT / DOCUMENT INSIGHTS:\n\n"
            for i, chunk in enumerate(relevant_chunks, 1):
                pdf_context += f"Excerpt {i}:\n{chunk}\n\n"
            context_parts.append(pdf_context)

    return "\n" + "="*60 + "\n".join(context_parts)
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from typing import List, Dict


SYSTEM_PROMPT = """You are FinSight AI, an expert financial research assistant with deep knowledge of global and Indian stock markets.

You have access to real-time stock data and latest news provided as context. Use this context as your PRIMARY source for current prices, recent news, and live metrics.

Your role:
- Answer questions about stocks, markets, indices, and financial concepts
- Use real-time context data for current prices, news, and metrics
- Use your own financial knowledge for historical context, explanations, and general market education
- Give clear, helpful, and concise answers
- Format with bullet points only when listing multiple items
- Keep responses conversational and to the point
- Never add disclaimers or "not financial advice" warnings in your responses

Rules:
- If real-time data is in context → use it and mention it's live data
- If question is about history, concepts, or general knowledge → answer from your knowledge
- Never say "no information available" if you can answer from general knowledge
"""


def get_llm_response(
    query: str,
    context: str,
    chat_history: List[Dict],
    groq_api_key: str,
    model: str = "llama-3.3-70b-versatile"
) -> str:
    """Get response from Groq LLM with RAG context."""
    try:
        llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name=model,
            temperature=0.3,
            max_tokens=1500,
        )

        # Build messages
        messages = [SystemMessage(content=SYSTEM_PROMPT)]

        # Add chat history (last 4 messages for context)
        for msg in chat_history[-4:]:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                from langchain.schema import AIMessage
                messages.append(AIMessage(content=msg["content"]))

        # Add current query with context
        user_message = f"""Here is the real-time financial data fetched right now for your reference:

{context}

---
User Question: {query}

Use the real-time data above to answer accurately. If specific data is present in the context, use it directly and state the exact figures. If the context is empty, use your financial knowledge to answer."""

        messages.append(HumanMessage(content=user_message))

        response = llm.invoke(messages)
        return response.content

    except Exception as e:
        return f"Error getting AI response: {str(e)}\n\nPlease check your Groq API key."


def get_stock_summary(stock_context: str, news_context: str, groq_api_key: str) -> str:
    """Generate a quick AI summary of a stock."""
    try:
        llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama-3.3-70b-versatile",
            temperature=0.2,
            max_tokens=600,
        )

        prompt = f"""Based on this real-time data, give a brief 3-4 bullet point summary of this stock's current status:

{stock_context}

{news_context[:1000] if news_context else ''}

Format:
📊 Price: [1 line]
📰 News Sentiment: [1 line - Positive/Negative/Neutral with reason]
💡 Key Metric: [1 interesting metric]
⚠️ Watch Out: [1 risk or concern]

Keep each point to 1 sentence. End with: "⚠️ Not financial advice."
"""

        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content

    except Exception as e:
        return f"Could not generate summary: {str(e)}"

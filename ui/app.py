"""
SmartOps Agent — Chainlit Chat Interface
TechShop Vietnam · Intelligent Customer Support

Run from the project root:
    chainlit run ui/app.py -w
"""

import sys
import os
import asyncio

# Ensure the project root is on the Python path so that
# 'agent', 'rag', 'mock_api' packages can be imported.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import chainlit as cl
from agent.agent import SmartOpsAgent


# ── Starter Suggestions ────────────────────────────────────────
# Quick-action buttons shown when the user first opens the chat

@cl.set_starters
async def set_starters():
    """Display suggested conversation starters for common workflows."""
    return [
        cl.Starter(
            label="📦 Track Order VN1024",
            message="Đơn hàng VN1024 giao đến đâu rồi?",
        ),
        cl.Starter(
            label="📚 Refund Policy",
            message="What is the refund policy for VNPay payments?",
        ),
        cl.Starter(
            label="💳 Check Transaction",
            message="Check transaction TXN-20250520-01133",
        ),
        cl.Starter(
            label="🎫 Report Defective Product",
            message="My order VN1027 headphones are defective. Please help.",
        ),
    ]


# ── Chat Start ──────────────────────────────────────────────────
# Initialize a new SmartOpsAgent instance per chat session

@cl.on_chat_start
async def on_chat_start():
    """Create a fresh agent with its own conversation memory for this session."""
    agent = SmartOpsAgent()
    cl.user_session.set("agent", agent)

    # Send a brief welcome message
    welcome = (
        "👋 **Xin chào! Welcome to TechShop Vietnam Support!**\n\n"
        "I'm your AI assistant. I can help you with:\n"
        "- 📦 Order tracking & delivery status\n"
        "- 💳 Payment & transaction inquiries\n"
        "- 🎫 Creating support tickets\n"
        "- 📚 Company policies & FAQs\n\n"
        "How can I assist you today?"
    )
    await cl.Message(content=welcome).send()


# ── Message Handler ─────────────────────────────────────────────
# Process each user message through the SmartOps Agent

@cl.on_message
async def on_message(message: cl.Message):
    """
    Invoke the SmartOps Agent with the user's message.
    
    Uses the LangchainCallbackHandler to automatically visualize
    tool calls (order lookup, ticket creation, etc.) as expandable
    steps in the Chainlit UI.
    """
    agent: SmartOpsAgent = cl.user_session.get("agent")

    if not agent:
        await cl.Message(
            content="⚠️ Session expired. Please refresh the page to start a new conversation."
        ).send()
        return

    # Chainlit's LangChain callback handler automatically creates
    # visual "Step" elements for each tool the agent invokes
    cb = cl.LangchainCallbackHandler(
        stream_final_answer=False,
    )

    try:
        # Run the synchronous agent executor in a background thread
        # so we don't block the Chainlit event loop
        res = await asyncio.to_thread(
            agent._executor.invoke,
            {"input": message.content},
            {"callbacks": [cb]},
        )

        output = res.get("output", "")

        if output:
            await cl.Message(content=output).send()
        else:
            await cl.Message(
                content="I'm sorry, I couldn't generate a response. Could you rephrase your question?"
            ).send()

    except Exception as e:
        error_msg = str(e)

        # Provide helpful context for common errors
        if "Connection" in error_msg or "refused" in error_msg:
            hint = (
                "\n\n💡 **Tip:** Make sure the Mock API server is running:\n"
                "```\nuvicorn mock_api.main:app --reload\n```"
            )
        elif "API" in error_msg or "key" in error_msg.lower():
            hint = (
                "\n\n💡 **Tip:** Check that your `GOOGLE_API_KEY` is set correctly in the `.env` file."
            )
        else:
            hint = ""

        await cl.Message(
            content=(
                f"⚠️ An error occurred while processing your request.\n\n"
                f"```\n{error_msg}\n```"
                f"{hint}"
            )
        ).send()

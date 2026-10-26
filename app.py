
import streamlit as st
from ddgs import DDGS

st.set_page_config(
    page_title="IAS Study Assistant",
    page_icon="🇮🇳",
    layout="centered"
)

st.title("🇮🇳 IAS Study Assistant")
st.caption("Your free-first UPSC learning companion")

if "messages" not in st.session_state:
    st.session_state.messages = []

def detect_subject(question):
    q = question.lower()
    subjects = {
        "Polity": ["constitution", "fundamental rights", "parliament",
                   "president", "supreme court", "preamble", "democracy"],
        "History": ["history", "gandhi", "mughal", "1857", "independence"],
        "Geography": ["river", "mountain", "monsoon", "soil", "climate"],
        "Economy": ["economy", "inflation", "gdp", "budget", "rbi", "tax"],
        "Environment": ["pollution", "biodiversity", "wildlife", "ecosystem"],
        "Science & Technology": ["science", "technology", "space", "isro"]
    }
    for subject, words in subjects.items():
        if any(word in q for word in words):
            return subject
    return "General Studies"

def answer_question(question):
    q = question.lower().strip(" !?.,")

    if q in ["hi", "hello", "hey"]:
        return "Hello! 👋 What UPSC topic would you like to study?"
    if q in ["thanks", "thank you", "thankyou", "thx"]:
        return "You're welcome! 😊 Happy to help with your UPSC preparation."
    if q in ["bye", "goodbye", "exit"]:
        return "Goodbye! Keep learning and best wishes for your preparation. 🇮🇳"

    subject = detect_subject(question)

    try:
        results = list(
            DDGS().text(
                question + " India UPSC official source",
                max_results=5
            )
        )
    except Exception:
        results = []

    summaries = [
        item.get("body", "").strip()
        for item in results
        if item.get("body", "").strip()
    ]

    sources = [
        (item.get("title", "Source"), item.get("href", ""))
        for item in results
        if item.get("title") and item.get("href")
    ]

    if not summaries:
        return (
            f"This appears to be a {subject} question. "
            "I couldn't retrieve web results just now. Please try again."
        )

    response = (
        f"**Subject: {subject}**\n\n"
        f"Here is an overview based on the information I found:\n\n"
        + "\n\n".join(summaries[:3])
        + "\n\n**UPSC study tip:** Identify the key concept, "
          "important facts, and its relevance to the syllabus."
    )

    if sources:
        response += "\n\n**Sources for further reading:**\n"
        for title, link in sources[:3]:
            response += f"\n- [{title}]({link})"

    return response

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask your UPSC question...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching for information..."):
            reply = answer_question(question)
        st.markdown(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

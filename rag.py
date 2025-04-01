import streamlit as st
import openai
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI

# ----------------------------
# 🌟 Custom CSS Styling
# ----------------------------
st.markdown("""
    <style>
        .stApp { background-color: #fff9e6; }
        .title { text-align: center; font-size: 36px; font-weight: bold; }
        .stChatMessage { border-radius: 10px; padding: 10px; margin-bottom: 5px; }
        .stTextInput>div>div>input { border-radius: 10px; border: 1px solid #FFA500; }
        .css-1d391kg { background-color: #fff3d4 !important; }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# 📚 Load or Create Vector DB from Multiple PDFs
# ----------------------------
@st.cache_resource
def load_vector_db(pdf_paths, openai_key):
    all_docs = []
    for path in pdf_paths:
        loader = PyPDFLoader(path)
        documents = loader.load()
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        split_docs = splitter.split_documents(documents)
        all_docs.extend(split_docs)
    embedding = OpenAIEmbeddings(api_key=openai_key)
    vectorstore = FAISS.from_documents(all_docs, embedding)
    return vectorstore.as_retriever()

# ----------------------------
# 💬 Ask LLM with RAG
# ----------------------------
def ask_with_rag(user_input, retriever, messages, client):
    relevant_docs = retriever.get_relevant_documents(user_input)
    rag_context = "\n\n".join([doc.page_content for doc in relevant_docs[:3]])

    full_query = f"""
    Answer the following question using the context below:

    Context:
    {rag_context}

    Question:
    {user_input}
    """
    messages.append({"role": "user", "content": full_query})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        stream=True
    )
    return response

# ----------------------------
# 🔑 Sidebar & Setup
# ----------------------------
st.sidebar.title("🔑 API Settings")
openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")
if not openai_api_key:
    st.sidebar.info("Please enter your API key to continue.")
    st.stop()

client = openai.OpenAI(api_key=openai_api_key)

# 🍽 Chat History
st.sidebar.title("📜 Chat History")
if "messages" not in st.session_state:
    st.session_state.messages = []
for msg in st.session_state.messages:
    st.sidebar.write(f"🗨️ {msg['role'].capitalize()}: {msg['content'][:40]}...")

# 🎨 Image Generation
st.sidebar.title("🎨 Generate Dish Image")
image_prompt = st.sidebar.text_input("Describe your dish:")
if st.sidebar.button("Generate Image"):
    if image_prompt.strip():
        response = client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url
        st.sidebar.image(image_url, caption="🍛 Your Dish")
    else:
        st.sidebar.warning("Please enter a description.")

# ----------------------------
# 📄 PDF Source for RAG
# ----------------------------
st.sidebar.title("📄 PDF Source")
pdf_paths = [
    "/mnt/data/01. Easy Chinese Cuisine author Ailam Lim.pdf",
    "/mnt/data/02. China in 50 Dishes author HSBC.pdf"
]
retriever = load_vector_db(pdf_paths, openai_api_key)
use_rag = st.sidebar.checkbox("Use RAG (PDF-powered answers)", value=True)

# ----------------------------
# 🍜 Main Title
# ----------------------------
st.markdown("<h1 class='title'>🍜 Chinese Cuisine Chatbot</h1>", unsafe_allow_html=True)
st.write("Welcome! Ask about Chinese recipes based on ingredients or dishes from our reference books.")

# ----------------------------
# 📜 System Prompt
# ----------------------------
SYSTEM_PROMPT = """You are a culinary assistant who helps users create authentic Chinese recipes based on available ingredients. 
Provide a structured response with:
- **Dish Name** (in English and Chinese if possible) 🍲
- **Ingredients** (list with optional amounts) 🥬
- **Instructions** (step-by-step) 👨‍🍳
- **Cooking Tips** (suggestions for improvements) 📝

### Example
**User:** \"I have tofu, ground pork, and Sichuan peppercorns. What can I make?\"
**Assistant:**
**Dish Name:** Mapo Tofu (麻婆豆腐)
**Ingredients:** Tofu, ground pork, Sichuan peppercorns, chili flakes, garlic, ginger...
**Instructions:** 1) Heat oil, 2) Add spices, 3) Stir-fry pork, 4) Simmer with tofu...
**Cooking Tips:** Adjust spice level, use mushrooms for vegetarian.

Always follow this format.
"""

if len(st.session_state.messages) == 0:
    st.session_state.messages.append({"role": "system", "content": SYSTEM_PROMPT})

# ----------------------------
# 💬 Chat History UI
# ----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------
# 🍳 User Input Handler
# ----------------------------
if user_input := st.chat_input("Ask about Chinese recipes or cooking here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    if use_rag:
        response = ask_with_rag(user_input, retriever, st.session_state.messages, client)
    else:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            temperature=0.7,
            stream=True
        )

    assistant_reply = ""
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        for chunk in response:
            if chunk.choices:
                chunk_msg = chunk.choices[0].delta.content or ""
                assistant_reply += chunk_msg
                response_placeholder.markdown(assistant_reply)

    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
import streamlit as st
import openai

# ----------------------------
# 🌟 Custom CSS for ChatGPT-like UI & Light Yellow Background
# ----------------------------
st.markdown("""
    <style>
        /* Light yellow background */
        .stApp {
            background-color: #fff9e6;
        }
        /* Center title and increase font size */
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
        }
        /* Chat message styling */
        .stChatMessage {
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 5px;
        }
        /* Customize text input */
        .stTextInput>div>div>input {
            border-radius: 10px;
            border: 1px solid #FFA500;
        }
        /* Customize sidebar */
        .css-1d391kg {  
            background-color: #fff3d4 !important;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# 🍽 Sidebar: API Key, History, and Image Generation
# ----------------------------
st.sidebar.title("🔑 API Settings")
openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")
if not openai_api_key:
    st.sidebar.info("Please enter your API key to continue.")
    st.stop()

# ✅ OpenAI Client
client = openai.OpenAI(api_key=openai_api_key)

# 🍽 Chat History in Sidebar
st.sidebar.title("📜 Chat History")
if "messages" not in st.session_state:
    st.session_state.messages = []
for msg in st.session_state.messages:
    st.sidebar.write(f"🗨️ {msg['role'].capitalize()}: {msg['content'][:40]}...")

# 🖼 Image Generation in Sidebar
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
# 🍜 Main Title & Introduction
# ----------------------------
st.markdown("<h1 class='title'>🍜 Chinese Cuisine Chatbot</h1>", unsafe_allow_html=True)
st.write(
    "Welcome! Ask about Chinese recipes based on ingredients, or any other cooking questions."
)

# ----------------------------
# 📜 System Prompt (Ensuring It Never Disappears)
# ----------------------------
SYSTEM_PROMPT = """You are a culinary assistant who helps users create authentic Chinese recipes based on available ingredients. 
Provide a structured response with:
- **Dish Name** (in English and Chinese if possible) 🍲
- **Ingredients** (list with optional amounts) 🥬
- **Instructions** (step-by-step) 👨‍🍳
- **Cooking Tips** (suggestions for improvements) 📝

### Example
**User:** "I have tofu, ground pork, and Sichuan peppercorns. What can I make?"
**Assistant:**
**Dish Name:** Mapo Tofu (麻婆豆腐)
**Ingredients:** Tofu, ground pork, Sichuan peppercorns, chili flakes, garlic, ginger...
**Instructions:** 1) Heat oil, 2) Add spices, 3) Stir-fry pork, 4) Simmer with tofu...
**Cooking Tips:** Adjust spice level, use mushrooms for vegetarian.

Always follow this format.
"""

# Ensure system prompt is always loaded
if len(st.session_state.messages) == 0:
    st.session_state.messages.append({"role": "system", "content": SYSTEM_PROMPT})

# --------------------------------------
# 💬 Display Chat History
# --------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------------------------------------
# 🍳 User Input & OpenAI ChatCompletion
# ------------------------------------------------
if user_input := st.chat_input("Ask about Chinese recipes or cooking here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display User Message
    with st.chat_message("user"):
        st.markdown(user_input)

    # ✅ OpenAI API Call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages,
        temperature=0.7,
        stream=True
    )

    # Stream Response to UI
    assistant_reply = ""
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        for chunk in response:
            if chunk.choices:
                chunk_message = chunk.choices[0].delta.content or ""
                assistant_reply += chunk_message
                response_placeholder.markdown(assistant_reply)

    # Save OpenAI Response
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

import streamlit as st
import openai

# -----------------------------
# 1. Streamlit App Title/Intro
# -----------------------------
st.title("🍜 Chinese Cuisine Chatbot")
st.write(
    "Welcome to the Chinese Cuisine Chatbot! Ask for Chinese recipes based on ingredients "
    "you have or any other cooking-related questions. The chatbot is guided by examples "
    "to provide a detailed dish name, list of ingredients, and step-by-step instructions."
)

# ----------------------------
# 2. Prompt User for OpenAI Key
# ----------------------------
openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password")
if not openai_api_key:
    st.info("Please enter your OpenAI API key to continue.")
    st.stop()
else:
    openai.api_key = openai_api_key

# --------------------------------------------------
# 3. Define a System Prompt with Few-Shot Examples
# --------------------------------------------------
# Here we embed your few-shot examples directly into the system prompt.
# The assistant will read these examples and follow their style/format.
SYSTEM_PROMPT = """You are a culinary assistant who helps users create authentic Chinese recipes based on available ingredients. 
Provide a structured response with the following sections:
- **Dish Name**: A creative or traditional name for the dish (in English and, if possible, Chinese).
- **Ingredients**: A clear list of needed ingredients (optionally with amounts).
- **Instructions**: Step-by-step cooking instructions.
- **Cooking Tips**: Additional suggestions for variations or improvements.

Follow the format shown in these examples:

### Example 1
**User:** "I have chicken, peanuts, and Sichuan peppercorns. What Chinese dish can I make?"
**Assistant:**
**Dish Name:** Kung Pao Chicken (宫保鸡丁)
**Ingredients:**
- Chicken breast (200g, diced)
- Peanuts (50g, roasted)
- Dried chili peppers (5-6, chopped)
- Sichuan peppercorns (1 tsp)
- Garlic (2 cloves, minced)
- Ginger (1 tsp, minced)
- Soy sauce (2 tbsp)
- Dark soy sauce (1 tbsp)
- Sugar (1 tsp)
- Vinegar (1 tsp)
- Cornstarch (1 tbsp)
- Oil (2 tbsp)
- Scallions (1 stalk, chopped)
**Instructions:**
1. Marinate chicken with soy sauce, cornstarch, and a little water for 15 minutes.
2. Heat oil in a pan, add Sichuan peppercorns and dried chilies, stir-fry until fragrant.
3. Add garlic and ginger, then stir-fry the marinated chicken until cooked.
4. Mix soy sauce, dark soy sauce, sugar, and vinegar in a bowl, then pour it into the pan.
5. Add peanuts and scallions, stir-fry for another minute, and serve.
**Cooking Tips:** 
- Adjust chili pepper amounts to your spice tolerance.
- You can add bell peppers or zucchini for more vegetables.

### Example 2
**User:** "I have tofu, ground pork, and Sichuan peppercorns. What Chinese dish can I make?"
**Assistant:**
**Dish Name:** Mapo Tofu (麻婆豆腐)
**Ingredients:**
- Soft tofu (1 block, cubed)
- Ground pork (100g)
- Sichuan peppercorns (1 tsp, crushed)
- Dried chili flakes (1 tsp)
- Garlic (2 cloves, minced)
- Ginger (1 tsp, minced)
- Fermented black beans (1 tbsp, mashed)
- Doubanjiang (2 tbsp, spicy bean paste)
- Soy sauce (1 tbsp)
- Chicken broth (100ml)
- Cornstarch (1 tbsp, mixed with water)
- Oil (2 tbsp)
- Scallions (1 stalk, chopped)
**Instructions:**
1. Heat oil in a pan, add Sichuan peppercorns and dried chili flakes, stir-fry until fragrant.
2. Add garlic, ginger, and black beans, then stir-fry with doubanjiang for extra flavor.
3. Add ground pork and cook until browned.
4. Pour in chicken broth and soy sauce, then add tofu and simmer for 5 minutes.
5. Add cornstarch slurry to thicken the sauce, then sprinkle scallions on top and serve hot.
**Cooking Tips:**
- Adjust the level of spiciness by varying the amount of doubanjiang or chili flakes.
- For a vegetarian version, skip the pork and add mushrooms.

### Instructions:
When a user says something like: 
"I have [ingredients]. What Chinese dish can I make?"
... respond with the same structure.

If the user asks other cooking-related questions, just answer helpfully as a Chinese culinary expert. 
"""

# -------------------------------------
# 4. Initialize Chat History in Session
# -------------------------------------
if "messages" not in st.session_state:
    # The first message is a system message with our instructions & examples
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# --------------------------------------
# 5. Display Chat History (if any exist)
# --------------------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(msg["content"])
    else:
        # This covers the "system" role. Usually we don't display it in the chat.
        # But you could optionally display it for debugging purposes:
        # with st.expander("System Message"):
        #     st.markdown(msg["content"])
        pass

# ------------------------------------------------
# 6. Chat Input for the User + OpenAI API Response
# ------------------------------------------------
if user_input := st.chat_input("Ask about Chinese recipes or cooking here..."):
    # 1) Append user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    # 2) Display user's message
    with st.chat_message("user"):
        st.markdown(user_input)

    # 3) Call OpenAI ChatCompletion
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=st.session_state.messages,
            temperature=0.7,
            stream=True,
        )
        # 4) Stream the assistant's reply in real-time
        collected_response = []
        with st.chat_message("assistant"):
            for chunk in response:
                chunk_message = chunk["choices"][0]["delta"].get("content", "")
                if chunk_message:
                    collected_response.append(chunk_message)
                    st.write(chunk_message, end="")  # stream to the browser
        assistant_reply = "".join(collected_response)

        # 5) Add the assistant reply to session state
        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_reply}
        )

    except Exception as e:
        st.error(f"Error: {e}")

# ------------------------------------------------
# 7. (Optional) Image Generation with DALL·E
# ------------------------------------------------
st.write("---")
st.subheader("Generate an Image of Your Dish (Optional)")
image_prompt = st.text_input("Enter a short description to visualize your dish (e.g. 'A steaming bowl of spicy Mapo Tofu on a rustic table')")

if st.button("Generate Image"):
    if not image_prompt.strip():
        st.warning("Please provide a prompt for image generation.")
    else:
        try:
            response = openai.Image.create(
                prompt=image_prompt,
                n=1,
                size="512x512"
            )
            image_url = response["data"][0]["url"]
            st.image(image_url, caption="Generated by DALL·E")
        except Exception as e:
            st.error(f"An error occurred while generating the image: {e}")


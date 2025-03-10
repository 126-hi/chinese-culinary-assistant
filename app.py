import streamlit as st
import openai
import os

# ========================
# Configure your API key
# ========================
# For production, load this from environment variables or Streamlit secrets.
openai.api_key = "your API Key"

# ===================
# Single-shot Prompt
# ===================
single_shot_prompt = """You are a culinary assistant who helps users create delicious Chinese recipes based on available ingredients. Provide a detailed response including:

1. **Dish Name** – A creative and appealing name for the dish.
2. **Ingredients List** – List all necessary ingredients.
3. **Cooking Steps** – Provide clear, step-by-step instructions.
4. **Cooking Tips** – Offer additional advice for variations or improvements.

### **User Input:**
"I have {ingredients}. What Chinese dish can I make?"

### **Expected Output:**"""

# ==================
# Few-shot Prompt
# ==================
few_shot_prompt = """You are a culinary assistant who helps users create authentic Chinese recipes based on available ingredients. Follow the given format and examples to generate an accurate response.

### Example 1:
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

### Example 2:
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
5. Add cornstarch slurry to thicken the sauce, then sprinkle scallions and serve hot.

### Example 3:
**User:** "I have pork, cabbage, and dumpling wrappers. What Chinese dish can I make?"
**Assistant:**
**Dish Name:** Jiaozi (Chinese Dumplings, 饺子)
**Ingredients:**
- Ground pork (200g)
- Napa cabbage (100g, finely chopped)
- Garlic (1 clove, minced)
- Ginger (1 tsp, minced)
- Soy sauce (2 tbsp)
- Sesame oil (1 tsp)
- Salt (to taste)
- Dumpling wrappers (20 pieces)
- Water (for sealing and boiling)
**Instructions:**
1. Mix ground pork, chopped cabbage, garlic, ginger, soy sauce, sesame oil, and salt in a bowl.
2. Place a small spoonful of filling in the center of each dumpling wrapper.
3. Wet the edges of the wrapper with water, fold in half, and seal tightly.
4. Boil a pot of water, add dumplings, and cook until they float (about 5 minutes).
5. Serve hot with soy sauce or black vinegar dipping sauce.

### Now it's your turn:
**User:** "I have {ingredients}. What Chinese dish can I make?"
**Assistant:**
"""

# =======================================
# Core function to generate recipes
# =======================================
def get_recipe(ingredients, mode="single-shot", model="gpt-4"):
    """
    Generates a recipe using either single-shot or few-shot prompts
    via OpenAI ChatCompletion.
    """
    if mode == "few-shot":
        prompt = few_shot_prompt.format(ingredients=ingredients)
    else:
        prompt = single_shot_prompt.format(ingredients=ingredients)

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful recipe assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"].strip()

# ============================================
# Conversational Chat Function with memory
# ============================================
def chat_with_gpt(user_message, model="gpt-4"):
    """
    Appends the user's message to the chat history in st.session_state,
    calls the OpenAI ChatCompletion endpoint, and saves the assistant's 
    response back into st.session_state. Returns the assistant's message.
    """
    st.session_state.chat_history.append({"role": "user", "content": user_message})
    response = openai.ChatCompletion.create(
        model=model,
        messages=st.session_state.chat_history,
        temperature=0.7
    )
    assistant_reply = response.choices[0].message.content.strip()
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply

# =========================================
# Image Generation (DALL·E)
# =========================================
def generate_image_from_text(prompt, size="512x512"):
    """
    Generates an image using the OpenAI Image (DALL·E) endpoint, 
    based on the provided text prompt. Returns the image URL if successful.
    """
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size=size
        )
        return response["data"][0]["url"]
    except Exception as e:
        st.error(f"An error occurred while generating the image: {e}")
        return None

# ==================
#   Streamlit App
# ==================
st.title("Culinary Assistant")
st.write("Generate Chinese recipes, create images of your dish, and chat with memory – all in one app.")

# Initialize session state for chat history and recipe text
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "generated_recipe" not in st.session_state:
    st.session_state.generated_recipe = None

# -----------------------------------------
# 1) Ingredient-based Recipe Generation
# -----------------------------------------
st.subheader("Generate a Recipe")

ingredients = st.text_input("Enter your ingredients (e.g., chicken, garlic, soy sauce):")
prompt_mode = st.radio(
    "Choose your prompt style:",
    ("Single-shot", "Few-shot"),
    horizontal=True
)
model_option = st.selectbox(
    "Choose the Chat model:",
    ("gpt-4", "gpt-3.5-turbo")
)

# Recipe generation button
if st.button("Generate Recipe"):
    if ingredients.strip():
        mode_selected = "few-shot" if prompt_mode == "Few-shot" else "single-shot"
        recipe_text = get_recipe(ingredients, mode=mode_selected, model=model_option)
        st.session_state.generated_recipe = recipe_text
    else:
        st.warning("Please enter some ingredients first!")

# Display the generated recipe if it exists
if st.session_state.generated_recipe:
    st.markdown("### Here's your recipe:")
    st.markdown(st.session_state.generated_recipe)

# --------------------------
# 2) Image Generation
# --------------------------
st.write("---")
st.subheader("Generate an Image of Your Dish (Optional)")

image_prompt = st.text_input("Describe how you'd like your dish to appear (e.g., 'A plate of Kung Pao Chicken in a rustic Chinese kitchen').")

if st.button("Generate Image"):
    if image_prompt.strip():
        image_url = generate_image_from_text(image_prompt, size="512x512")
        if image_url:
            st.image(image_url, caption="Generated Image")
    else:
        st.warning("Please enter an image description first!")

# --------------------------
# 3) Conversational Chat
# --------------------------
st.write("---")
st.subheader("Conversational Chat")
st.write("Ask the Culinary Assistant about anything related to cooking or beyond, with context retained.")

user_chat_input = st.text_input("Enter your message to chat with the assistant:")

if st.button("Send Message"):
    if user_chat_input.strip():
        chat_reply = chat_with_gpt(user_chat_input, model=model_option)
        st.write(f"**Assistant:** {chat_reply}")
    else:
        st.warning("Please enter a message first!")

# Display conversation history
if st.session_state.chat_history:
    st.write("### Conversation History")
    for idx, msg in enumerate(st.session_state.chat_history):
        if msg["role"] == "user":
            st.markdown(f"**User:** {msg['content']}")
        else:
            st.markdown(f"**Assistant:** {msg['content']}")

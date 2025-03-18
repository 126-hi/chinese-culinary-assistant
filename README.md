
# chinese-culinary-assistant

A **Streamlit** application that leverages **OpenAI** APIs to:
- Generate Chinese recipes (via single-shot or few-shot prompts).
- Create dish images using the DALL·E endpoint.
- Maintain conversational context through `st.session_state`.

## Features

1. **Recipe Generation**  
   - **Single-shot Prompt**: Quick recipe suggestions by simply listing ingredients.  
   - **Few-shot Prompt**: Provides more detailed, context-rich recipes (including dish name, ingredients, steps, and tips).

2. **Image Generation**  
   - Generate dish images using OpenAI’s **DALL·E** based on a text prompt.

3. **Conversational Chat**  
   - Saves the conversation in `st.session_state`, allowing a dynamic Q&A style chat without losing context.

## Installation

1. **Clone or Download** this repository to your local environment:
   ```bash
   git clone https://github.com/126-hi/chinese-culinary-assistant.git
   cd chinese-culinary-assistant
   ```
2. **Install Dependencies**:
   ```bash
   pip install streamlit openai
   ```

## Usage

1. **Run** the app locally with:
   ```bash
   streamlit run app.py
   ```
2. Enter your **OpenAI API Key** when prompted (in the sidebar by default).
3. Start **chatting** to receive recipe suggestions or use the **image generation** feature to visualize your dish ideas.

## Screenshots

> Below are some placeholder screenshots; replace the URLs with actual links to your images.

- **Main Interface**  
  ![Main Interface](https://raw.githubusercontent.com/126-hi/chinese-culinary-assistant/7b2ff37032252fe3857ae6f647b9f2175e4e5650/%E6%88%AA%E5%B1%8F2025-03-17%2021.25.47.png)

- **Recipe Generation**  
  ![Recipe Generation](https://raw.githubusercontent.com/126-hi/chinese-culinary-assistant/7b2ff37032252fe3857ae6f647b9f2175e4e5650/%E6%88%AA%E5%B1%8F2025-03-17%2021.26.46.png)

- **Image Generation**  
  ![Generated Dish Image](https://raw.githubusercontent.com/126-hi/chinese-culinary-assistant/7b2ff37032252fe3857ae6f647b9f2175e4e5650/%E6%88%AA%E5%B1%8F2025-03-17%2021.27.33.png)

## License

Licensed under the [MIT License](LICENSE).

---

**Happy Cooking!** 




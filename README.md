# chinese-culinary-assistant

A simple Streamlit application that uses OpenAI's APIs for:

- Generating Chinese recipes (using single-shot or few-shot prompts).
- Creating images via OpenAI’s Image (DALL·E) endpoint.
- Conversational chat with memory, thanks to `st.session_state`.

## Features

1. **Recipe Generation**
   - **Single-shot Prompt**: Quick recipe suggestions without examples.
   - **Few-shot Prompt**: More detailed, context-rich recipes with provided examples.

2. **Image Generation**
   - Generates images based on a text prompt using DALL·E.

3. **Conversational Chat**
   - Retains conversational context in `st.session_state` so the user can have a back-and-forth conversation without losing previous context.

## Installation

1. Clone or download the repository to your local machine.
2. Install the required Python packages:

   ```bash
   pip install streamlit openai
   ```

## Usage

Run the Streamlit app locally:

```bash
streamlit run app.py
```

## Demo / Screenshots

Here are some placeholder images to illustrate the UI. Replace them with your actual screenshots once you have them:

### 1. Main Page
*(Add your screenshot here)*
<img width="910" alt="Image" src="https://github.com/user-attachments/assets/3c041efc-7e90-4b39-9f8a-ec146d098a23" />

### 2. Recipe Generation
<img width="892" alt="Image" src="https://github.com/user-attachments/assets/34b64ebd-9669-4eb1-ab91-8f944165cfc4" />

<img width="855" alt="Image" src="https://github.com/user-attachments/assets/889974ad-7392-4201-bdb9-d155ebfdd12f" />

### 3. Image Generation
<img width="852" alt="Image" src="https://github.com/user-attachments/assets/23511c78-9f40-454d-aec2-fed409dbefe3" />



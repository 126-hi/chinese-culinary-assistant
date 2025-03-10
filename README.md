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

### 2. Recipe Generation
*(Add your screenshot here)*

### 3. Conversational Chat
*(Add your screenshot here)*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork this repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

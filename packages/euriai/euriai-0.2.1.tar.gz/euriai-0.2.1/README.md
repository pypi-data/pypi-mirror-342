# euriai 🧠

**EURI AI Python Client** – A simple wrapper and CLI tool for the [Euron LLM API](https://api.euron.one).  
Supports completions, streaming responses, CLI interaction, and an interactive guided wizard!

---

## 🔧 Installation

```bash
pip install euriai

## python sample Usage

from euriai import EuriaiClient

client = EuriaiClient(
    api_key="your_api_key_here",
    model="gpt-4.1-nano"  # You can also try: "gemini-2.0-flash-001", "llama-4-maverick", etc.
)

response = client.generate_completion(
    prompt="Write a short poem about artificial intelligence.",
    temperature=0.7,
    max_tokens=300
)

print(response)


## 💻 Command-Line Interface (CLI) Usage
Run prompts directly from the terminal:

euriai --api_key YOUR_API_KEY --prompt "Tell me a joke"


## Enable streaming output (if supported by the model):

euriai --api_key YOUR_API_KEY --prompt "Stream a fun fact" --stream


##List all supported model IDs with recommended use-cases and temperature/token advice:

euriai --models


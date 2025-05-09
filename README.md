# Set up Environment & Install ADK
## Create & Activate Virtual Environment (Recommended):
```
# Create
python -m venv .venv
# Activate (each new terminal)
# macOS/Linux: source .venv/bin/activate
# Windows CMD: .venv\Scripts\activate.bat
# Windows PowerShell: .venv\Scripts\Activate.ps1
```

## Install ADK and Lite LLM:
```
pip install google-adk
pip install litellm
```

# Set up the model
Touch .env file in agent dir
## Vertex AI
```
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
GOOGLE_CLOUD_LOCATION=LOCATION
```
## API Keys
```
# Set to False to use API keys directly (required for multi-model)
GOOGLE_GENAI_USE_VERTEXAI=FALSE

# --- Replace with your actual keys ---
GOOGLE_API_KEY=PASTE_YOUR_ACTUAL_GOOGLE_API_KEY_HERE
ANTHROPIC_API_KEY=PASTE_YOUR_ACTUAL_ANTHROPIC_API_KEY_HERE
OPENAI_API_KEY=PASTE_YOUR_ACTUAL_OPENAI_API_KEY_HERE
# --- End of keys ---
```

# Run Your Agent
## Run the following command to launch the dev UI.
```
adk web
```

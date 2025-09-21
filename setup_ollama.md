# Ollama Setup for Jarvis

## Install Ollama
```bash
# macOS
brew install ollama

# Or download from https://ollama.ai
```

## Start Ollama Service
```bash
ollama serve
```

## Pull Gemma Model
```bash
ollama pull gemma:2b
```

## Verify Setup
```bash
ollama list
# Should show gemma:2b model
```

The system will now use local Ollama instead of HuggingFace API.
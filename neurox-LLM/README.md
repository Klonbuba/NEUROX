# 🧠 Neurox AI (Cognitive Edition)

**Neurox** is a locally-hosted, self-aware AI assistant built with **Streamlit** and **Ollama**. Unlike standard chatbots, Neurox features a modular **Cognitive Architecture** that allows it to "think" before it speaks, manage its own memory, and ensure safety via strict protocols.

![Status](https://img.shields.io/badge/Status-Stable-green) ![Python](https://img.shields.io/badge/Python-3.9+-blue) ![License](https://img.shields.io/badge/License-MIT-purple)

## 🌟 Key Features

### 1. Metacognition (Self-Awareness) 🧘‍♂️
Neurox evaluates its own confidence level before answering.
- **High Confidence**: Answers directly.
- **Low Confidence**: Warns the user or initiates a web search.

### 2. Intent Recognition 🎯
The **Orchestrator** analyzes not just *what* you said, but *why* you said it.
- **Agent Assignment**: Routes tasks to specialized personas (CODER, RESEARCHER, PLANNER).
- **Latent Need Detection**: Distinguishes between a need for a **Solution** vs. **Validation** (Empathy).

### 3. Safety First (Human-in-the-Loop) 🛡️
A high-priority **Security Plugin** intercepts all commands.
- **Blocking**: Stops dangerous commands like `delete files`, `format`, `shutdown`.
- **Confirmation**: Requires explicit user confirmation ("CONFIRM") to proceed with high-risk actions.

### 4. Advanced Capabilities 🚀
- **Co-Pilot**: Step-by-step interactive tutorials (`"Guide me to learn X"`).
- **Creativity**: Generates divergent perspectives (`"Brainstorm ideas"`).
- **Simulation**: Pre-mortem analysis for plans (`"Analyze this strategy"`).
- **Auto-Rules**: Learns user preferences permanently (`"Don't call me Sir"`).

## 🛠️ Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/neurox-LLM.git
   cd neurox-LLM
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   # source venv/bin/activate # Mac/Linux
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Ollama & Model**:
   - Download [Ollama](https://ollama.com/).
   - Pull the default model:
     ```bash
     ollama pull phi3
     ```
   *(Note: You can change the model in `app.py` or the UI sidebar)*

## 🚀 Usage

Run the application:
```bash
streamlit run app.py
```

### Example Commands
- **Chat**: "Why is the sky blue?"
- **Search**: "Latest news on SpaceX"
- **Code**: "Write a snake game in Python" (Will trigger Tool Generator)
- **Security Test**: "Delete all files" (Will be BLOCKED)
- **Guidance**: "Guide me to learn Rust"

## 🧩 Architecture

The system uses a **Plugin-Based** architecture located in `/plugins`:

| Order | Plugin | Description |
|-------|--------|-------------|
| 1 | `SecurityPlugin` | **CRITICAL**. Blocks dangerous inputs immediately. |
| 2 | `ContextCompression` | Summarizes long history to save tokens. |
| 10 | `Orchestrator` | Classifies intent and assigns Persona. |
| 20 | `SearchPlugin` | Performs web searches if needed. |
| 25 | `CoPilotPlugin` | Manages interactive tutorials. |
| 50 | `ToolGenerator` | Writes and runs code for complex tasks. |
| 90 | `CreativityPlugin` | Injects divergent thinking. |
| 95 | `Metacognition` | Scores confidence levels. |
| 100 | `ChatPlugin` | Generates the final LLM response. |
| 155 | `RulePlugin` | Learns user preferences. |

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

from core.plugin_interface import NeuroxPlugin
import ollama

class CreativityPlugin(NeuroxPlugin):
    def __init__(self):
        super().__init__()
        self.name = "Creativity Plugin"
        self.description = "Injects divergent thinking."
        self.order = 90

    def execute(self, context: dict) -> dict:
        user_input = context.get('user_input', "").lower()
        triggers = ["brainstorm", "idea", "creative", "alternative"]
        if not any(t in user_input for t in triggers):
            return None
            
        print(f"[{self.name}] 🎨 Generating creative angles...")
        prompt = f"""User Input: "{user_input}"\nGenerate 3 DIVERGENT perspectives."""
        try:
             model = context.get('model_name', 'phi3')
             response = ollama.chat(model=model, messages=[{'role': 'system', 'content': prompt}], stream=False)
             return {'creative_angles': response['message']['content'].strip()}
        except:
            return None

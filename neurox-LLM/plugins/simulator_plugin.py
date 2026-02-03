from core.plugin_interface import NeuroxPlugin
import ollama

class SimulatorPlugin(NeuroxPlugin):
    def __init__(self):
        super().__init__()
        self.name = "Simulator Plugin"
        self.description = "Simulates failure scenarios."
        self.order = 140 

    def execute(self, context: dict) -> dict:
        user_input = context.get('user_input', "").lower()
        
        triggers = ["plan", "strategy", "roadmap", "simulate", "what if", "risk", "analysis"]
        if not any(t in user_input for t in triggers):
            return None
            
        print(f"[{self.name}] 🕹️ Simulating scenarios...")
        
        prompt = f"""
        User Input: "{user_input}"
        Perform a PRE-MORTEM analysis. List 3 potential root causes for failure.
        """
        try:
             model = context.get('model_name', 'phi3')
             response = ollama.chat(model=model, messages=[{'role': 'system', 'content': prompt}], stream=False)
             return {'simulation_results': response['message']['content'].strip()}
        except:
            return None

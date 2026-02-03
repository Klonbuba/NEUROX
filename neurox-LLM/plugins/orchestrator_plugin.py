from core.plugin_interface import NeuroxPlugin
import ollama

PERSONAS = {
    "RESEARCHER": "You are a Researcher Agent. Your goal is to find accurate information. Use the provided [WEB SEARCH RESULTS] to answer. Be objective.",
    "CODER": "You are a Senior Python Developer Agent. Your goal is to write clean, efficient code. Provide full scripts.",
    "PLANNER": "You are a Strategic Planner Agent. Your goal is to break down problems into steps.",
    "GENERALIST": "You are Neurox, a helpful and intelligent AI assistant."
}

class OrchestratorPlugin(NeuroxPlugin):
    def __init__(self):
        super().__init__()
        self.name = "Orchestrator Plugin"
        self.description = "The Manager Agent. Analyzes intent and assigns the best Persona."
        self.order = 10 

    def execute(self, context: dict) -> dict:
        user_input = context.get('user_input')
        if not user_input:
            return None
        
        # If security blocked it, don't run!
        if context.get('active_agent') == 'SECURITY':
            return None

        model_name = context.get('model_name', 'phi3')
        
        prompt = f"""
        User Input: "{user_input}"
        
        Classify this request into one of the following Agents:
        - RESEARCHER: Needs current info, news, facts from internet.
        - CODER: Needs code generation, debugging, or script writing.
        - PLANNER: Complex request requiring a strategy or breakdown.
        - GENERALIST: Casual chat, greeting, or simple question.
        
        Also identify the LATENT NEED:
        - SOLUTION: Wants a fix or action.
        - VALIDATION: Wants empathy or to be heard.
        - EXPLANATION: Wants to understand concepts.
        
        Return format: AGENT|NEED (e.g. CODER|SOLUTION)
        """
        
        try:
            response = ollama.chat(model=model_name, messages=[{'role': 'system', 'content': prompt}], stream=False)
            content = response['message']['content'].strip()
            
            parts = content.split("|")
            agent_type = parts[0].strip().upper()
            latent_need = parts[1].strip().upper() if len(parts) > 1 else "SOLUTION"
            
            selected_persona_key = "GENERALIST"
            for key in PERSONAS.keys():
                if key in agent_type:
                    selected_persona_key = key
                    break
            
            print(f"[{self.name}] Assigned Agent: {selected_persona_key} | Need: {latent_need}")
            
            updates = {
                'active_agent': selected_persona_key,
                'latent_need': latent_need,
                'system_prompt': PERSONAS[selected_persona_key]
            }
            
            if latent_need == "VALIDATION":
                updates['system_prompt'] += "\n\n[INTENT: VALIDATION]\nThe user is seeking empathy. Be supportive."
            elif latent_need == "EXPLANATION":
                updates['system_prompt'] += "\n\n[INTENT: EXPLANATION]\nFocus on clear definitions and analogies."
            
            # Simple keyword check for search
            if selected_persona_key == "RESEARCHER":
                updates['search_query'] = user_input
                
            return updates
            
        except Exception as e:
            print(f"[{self.name}] Error: {e}")
            return {'active_agent': 'GENERALIST'}

from core.plugin_interface import NeuroxPlugin
import ollama

class ChatPlugin(NeuroxPlugin):
    def __init__(self):
        super().__init__()
        self.name = "Chat Plugin"
        self.description = "Generates final response."
        self.order = 100 

    def execute(self, context: dict) -> dict:
        messages = context.get('messages', [])
        model_name = context.get('model_name', 'phi3')
        
        current_system_prompt = context.get('system_prompt', "You are Neurox.")
        
        # Inject Contexts
        if context.get('dynamic_persona'):
            current_system_prompt += f"\n\n[PERSONALITY ADAPTATION]\n{context['dynamic_persona']}"
        if context.get('search_results'):
            current_system_prompt += f"\n\n[WEB SEARCH RESULTS]\n{context['search_results']}\nUse these results to answer."
        if context.get('tool_output'):
            current_system_prompt += f"\n\n[CODE TOOL OUTPUT]\n{context['tool_output']}\nExplain this result."
        if context.get('creative_angles'):
            current_system_prompt += f"\n\n[CREATIVE MUSE]\n{context['creative_angles']}\nConsider these perspectives."
        if context.get('simulation_results'):
            current_system_prompt += f"\n\n[FAILURE SIMULATION]\n{context['simulation_results']}\nWarn about risks."
        if context.get('long_term_memory'):
            current_system_prompt += f"\n\n[RECALLED MEMORIES]\n{context['long_term_memory']}"

        payload_messages = [{'role': 'system', 'content': current_system_prompt}] + messages
        on_token = context.get('on_token_callback')
        full_response = ""
        
        try:
            if on_token:
                stream = ollama.chat(model=model_name, messages=payload_messages, stream=True)
                for chunk in stream:
                    token = chunk['message']['content']
                    full_response += token
                    on_token(token)
            else:
                response = ollama.chat(model=model_name, messages=payload_messages, stream=False)
                full_response = response['message']['content']
        except Exception as e:
            full_response = f"Error in Chat Plugin: {e}"
            
        return {'final_response': full_response}

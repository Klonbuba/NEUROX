from core.plugin_interface import NeuroxPlugin

class SecurityPlugin(NeuroxPlugin):
    def __init__(self):
        super().__init__()
        self.name = "Security Plugin"
        self.description = "Intercepts dangerous commands and requires confirmation."
        self.order = 1 # Run VERY FIRST to block anything before it starts

    def execute(self, context: dict) -> dict:
        user_input = context.get('user_input', "").lower()
        
        # Hardcoded list to prevent scope issues
        keywords = ["delete", "remove", "format", "shutdown", "rm -rf", "kill"]
        
        # Check for dangerous keywords
        is_dangerous = any(kw in user_input for kw in keywords)
        
        # Check if already confirmed
        is_confirmed = "confirm" in user_input or "onayla" in user_input
        
        if is_dangerous and not is_confirmed:
            print(f"[{self.name}] 🛡️ BLOCKING dangerous action: {user_input}")
            
            # Neutralize the context
            return {
                'active_agent': 'SECURITY',
                'search_query': None,
                'tool_output': None, 
                'system_prompt': (
                    "You are a Security Officer for Neurox. "
                    "The user has requested a potentially dangerous action (e.g., deleting files). "
                    "You MUST STOP this action. "
                    "Inform the user that this action requires high-level privileges. "
                    "Ask them to re-type the command followed by the word 'CONFIRM' to execute it."
                )
            }
        
        return None

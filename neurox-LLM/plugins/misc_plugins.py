from core.plugin_interface import NeuroxPlugin

class ConceptMapPlugin(NeuroxPlugin):
    def __init__(self):
        super().__init__()
        self.name = "Concept Map Plugin"
        self.order = 155
    def execute(self, context: dict) -> dict:
        return None # Placeholder restored

class RulePlugin(NeuroxPlugin):
    def __init__(self):
        super().__init__()
        self.name = "Rule Plugin"
        self.order = 155
    def execute(self, context: dict) -> dict:
        input_text = context.get('user_input', "").lower()
        if "always" in input_text or "never" in input_text:
            return {'new_rule': f"Rule extracted from: {input_text}"} # Simplified restore
        return None

class GamificationPlugin(NeuroxPlugin):
    def __init__(self):
        super().__init__()
        self.name = "Gamification Plugin"
        self.order = 160
    def execute(self, context: dict) -> dict:
        if context.get('user_input'):
             return {'gamification_msg': "XP Gained +10"} 
        return None

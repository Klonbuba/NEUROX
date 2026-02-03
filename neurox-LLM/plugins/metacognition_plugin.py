from core.plugin_interface import NeuroxPlugin

class MetacognitionPlugin(NeuroxPlugin):
    def __init__(self):
        super().__init__()
        self.name = "Metacognition Plugin"
        self.description = "Evaluates context quality."
        self.order = 95 

    def execute(self, context: dict) -> dict:
        has_search = bool(context.get('search_results'))
        user_input = context.get('user_input', "").lower()
        complexity = any(kw in user_input for kw in ["explain", "analyze", "why"])
        
        meta = ""
        level = "HIGH"
        
        if not has_search:
            if complexity:
                level = "LOW"
                meta = "META-INSTRUCTION: Missing context. Admit you are relying on training data."
            else:
                 level = "MEDIUM"
        else:
            meta = "META-INSTRUCTION: Verify answer against [WEB SEARCH RESULTS]."
            
        existing = context.get('dynamic_persona', "")
        return {'dynamic_persona': existing + f"\n\n[METACOGNITION: {level}]\n{meta}"}

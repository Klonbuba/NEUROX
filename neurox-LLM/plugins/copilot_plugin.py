from core.plugin_interface import NeuroxPlugin

class CoPilotPlugin(NeuroxPlugin):
    def __init__(self):
        super().__init__()
        self.name = "CoPilot Plugin"
        self.description = "Provides step-by-step guidance."
        self.order = 25

    def execute(self, context: dict) -> dict:
        user_input = context.get('user_input', "").lower()
        if "guide me" in user_input or "tutorial" in user_input:
            return {'copilot_msg': f"🚀 Co-Pilot Activated: Guidance started."}
        return None

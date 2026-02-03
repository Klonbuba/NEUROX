from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.plugin_manager import PluginManager
import uvicorn

app = FastAPI(title="Neurox Core API")

manager = PluginManager()
manager.discover_plugins()

class ChatRequest(BaseModel):
    user_input: str
    model_name: str = "phi3"

@app.post("/chat")
def chat(request: ChatRequest):
    context = {
        'user_input': request.user_input,
        'model_name': request.model_name,
        'messages': []
    }
    try:
        final_context = manager.execute_all(context)
        return {
            "response": final_context.get('final_response', "No response"),
            "agent": final_context.get('active_agent', "UNKNOWN")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

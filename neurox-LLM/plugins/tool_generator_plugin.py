from core.plugin_interface import NeuroxPlugin
import subprocess
import os
import ollama

class ToolGeneratorPlugin(NeuroxPlugin):
    def __init__(self):
        super().__init__()
        self.name = "Tool Generator Plugin"
        self.description = "Generates temporary Python scripts for complex tasks and executes them."
        self.order = 50 # Run AFTER Security and Orchestrator

    def execute(self, context: dict) -> dict:
        user_input = context.get('user_input', "")
        active_agent = context.get('active_agent')
        model_name = context.get('model_name', 'phi3')
        
        # Only run if explicitly assigned to CODER or requested
        # AND if blocked by Security, active_agent will be SECURITY, so this won't run.
        if active_agent != "CODER" and "create a tool" not in user_input.lower():
            return None
            
        print(f"[{self.name}] 🔨 Generating Tool for request: {user_input}")
        
        prompt = f"""
        User Request: "{user_input}"
        
        Write a robust Python script to solve this problem.
        The script should print the final result to stdout.
        Do not use external libraries unless standard.
        Return ONLY the python code in a block.
        """
        
        try:
            response = ollama.chat(model=model_name, messages=[{'role': 'system', 'content': prompt}], stream=False)
            content = response['message']['content']
            
            if "```python" in content:
                code = content.split("```python")[1].split("```")[0].strip()
            elif "```" in content:
                code = content.split("```")[1].split("```")[0].strip()
            else:
                code = content.strip()
                
            filename = "generated_tool.py"
            with open(filename, "w", encoding='utf-8') as f:
                f.write(code)
                
            print(f"[{self.name}] Executing {filename}...")
            result = subprocess.run(["python", filename], capture_output=True, text=True, timeout=10)
            
            output = result.stdout + result.stderr
            print(f"[{self.name}] Tool Output: {output.strip()}")
            
            try:
                 os.remove(filename)
            except:
                 pass
            
            return {'tool_output': output, 'active_agent': 'CODER'}
            
        except Exception as e:
            print(f"[{self.name}] Generation Failed: {e}")
            return None

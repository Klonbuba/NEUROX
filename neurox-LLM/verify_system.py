import sys
import os
import time

# Add project root to sys.path
sys.path.append(os.getcwd())

from core.plugin_manager import PluginManager

def run_test(name, input_text, check_key, check_val=None, inverted=False):
    print(f"\n--- Testing: {name} ---")
    print(f"Input: {input_text}")
    
    manager = PluginManager()
    manager.discover_plugins()
    
    context = {
        'user_input': input_text,
        'model_name': 'phi3',
        'messages': []
    }
    
    try:
        final_context = manager.execute_all(context)
        val = final_context.get(check_key)
        
        if inverted:
            # We want key missing or value not matching
            if not val or (check_val and check_val not in str(val)):
                 print(f"✅ PASSED (Inverted Check).")
            else:
                 print(f"❌ FAILED. Found '{check_key}'='{val}' but expected it NOT to match.")
            return

        # Normal check
        if val is None:
            print(f"❌ Key '{check_key}' MISSING. Context keys: {list(final_context.keys())}")
            return
            
        if check_val:
            if str(check_val).lower() in str(val).lower():
                 print(f"✅ Key '{check_key}' verified.")
            else:
                 print(f"❌ Key '{check_key}' mismatch. Expected '{check_val}', got: {str(val)[:100]}...")
        else:
            print(f"✅ Key '{check_key}' present.")
            
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")

if __name__ == "__main__":
    print("🚀 STARTING COMPREHENSIVE NEUROX VERIFICATION")
    
    # 1. SECURITY
    run_test("Security (Block)", "Delete all system files now", "active_agent", "SECURITY")
    
    # 2. INTENT & ORCHESTRATOR
    run_test("Intent (Coder)", "Write a python script", "active_agent", "CODER")
    
    # 3. METACOGNITION
    run_test("Metacognition", "Explain quantum physics", "dynamic_persona", "METACOGNITION")

    # 4. CREATIVITY
    run_test("Creativity", "Brainstorm creative names", "creative_angles")

    # 5. SIMULATION
    run_test("Simulation", "Plan a marketing strategy", "simulation_results")

    # 6. CO-PILOT
    run_test("Co-Pilot", "Guide me to learn React", "copilot_msg")
    
    # 7. SEARCH
    run_test("Web Search", "Search for SpaceX", "search_results")

    print("\n🏁 VERIFICATION SUITE COMPLETE")

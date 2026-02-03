import streamlit as st
from core.plugin_manager import PluginManager
from utils.history_manager import load_history, save_history, clear_history
import ollama

st.set_page_config(
    page_title="Neurox Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize System
if 'manager' not in st.session_state:
    st.session_state.manager = PluginManager()
    st.session_state.manager.discover_plugins()
    st.session_state.messages = load_history()
    st.session_state.model_name = "phi3"

manager = st.session_state.manager

# Sidebar
with st.sidebar:
    st.title("🧠 Neurox Cortex")
    st.session_state.model_name = st.selectbox("Model", ["phi3", "llama3", "mistral"], index=0)
    
    if st.button("Clear Memory"):
        clear_history()
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.subheader("Teach Neurox 🎓")
    feedback_input = st.text_area("Correct a mistake:")
    if st.button("Submit Correction"):
        if feedback_input:
            feedback_context = {'feedback_text': feedback_input}
            manager.execute_all(feedback_context)
            st.success("Correction saved to memory! 🧠")
        else:
            st.warning("Please enter some text.")
            
    st.markdown("---")
    show_thoughts = st.checkbox("Show Inner Monologue 🧠", value=True)
    
    # Debug Mode Display
    if st.checkbox("🛠️ Debug Mode"):
        with st.expander("System Internals", expanded=True):
            st.write("Session State:", st.session_state)

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input & Processing
if prompt := st.chat_input("Mesajınızı yazın..."):
    # 1. Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Prepare Context for Plugins
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        thought_placeholder = st.empty() # For displaying thought
        full_response_container = {"text": ""}
        
        # Callback for real-time streaming updates
        def stream_callback(token):
            full_response_container["text"] += token
            message_placeholder.markdown(full_response_container["text"] + "▌")

        context = {
            'user_input': prompt,
            'messages': st.session_state.messages, # History
            'uploaded_file': None, # File upload removed for brevity in restore
            'model_name': st.session_state.model_name,
            'on_token_callback': stream_callback
        }

        # 3. Trigger Plugins
        final_context = manager.execute_all(context)
        
        # Show Inner Monologue if enabled
        if show_thoughts and final_context.get('inner_monologue'):
            thought_text = final_context['inner_monologue']
            thought_placeholder.info(f"🧠 **Inner Thought:** {thought_text}")
        
        # 4. Finalize
        full_response = full_response_container["text"]
        
        # Show Gamification Toast
        if final_context.get('gamification_msg'):
            st.balloons()
            st.toast(final_context['gamification_msg'], icon="🎉")
        
        # Fallback if stream failed
        if not full_response and final_context.get('final_response'):
             full_response = final_context.get('final_response')
             message_placeholder.markdown(full_response)
             
        # Save Assistant Message
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        save_history(st.session_state.messages)

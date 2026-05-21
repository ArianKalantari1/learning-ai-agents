import streamlit as st
from agent_lvl2 import run_agent, load_history, save_history

# Page Config
st.set_page_config(page_title="Level 2 Agent", page_icon="🤖")
st.title("Level 2 Agent with Tools")

# Load history once into session state
if "messages" not in st.session_state:
    st.session_state.messages = load_history()

# Display conversation history
for message in st.session_state.messages:
    if isinstance(message["content"], str):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Handle new input
if prompt := st.chat_input("Ask me anything to calculate!"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = run_agent(prompt, st.session_state.messages)
        if reply:
            st.markdown(reply)
        else:
            st.markdown("Sorry, something went wrong.")

    save_history(st.session_state.messages)
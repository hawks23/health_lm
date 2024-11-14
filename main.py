import os
import streamlit as st 
from streamlit_chat import message
from agent import agent_executor
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

if 'history' not in st.session_state:
    st.session_state['history'] = []

st.title("Healthcare Chatbot")

# Outer container for the entire chat interface including the input field
with st.container():
    # Sub-container for chat history
    chat_container = st.container()
    with chat_container:
        # Display chat history
        for entry in st.session_state['history']:
            if entry['role'] == 'user':
                message(entry['content'], is_user=True)
            else:
                message(entry['content'])

    # Text input at the very bottom
    input_container = st.container()
    with input_container:
        with st.form("chat_form", clear_on_submit=True):
            question = st.text_input("Type your message...")
            submit_button = st.form_submit_button("Send")

            if submit_button and question:
                # Display user input immediately
                st.session_state['history'].append({"role": "user", "content": question})
                with chat_container:
                    message(question, is_user=True)
                
                # Placeholder for loading spinner
                with st.spinner("Thinking..."):
                    # Invoke the agent to get a response
                    response = agent_executor.invoke({"input": question})
                    response_text = response["output"]

                    # Display response and update history
                    st.session_state['history'].append({"role": 'bot', "content": response_text})
                    with chat_container:
                        message(response_text)

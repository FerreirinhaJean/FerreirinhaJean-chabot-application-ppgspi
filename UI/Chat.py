import streamlit as st
from chat.AgentConversation import AgentConversation
import os
from LLM.LLM import AzureOpenAI
import time

class Chat():
    
    def __init__(self) -> None:
        self.__azure_openai = AzureOpenAI(
            os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            os.getenv("AZURE_OPENAI_DEPLOYMENT_EMBEDDING")
        )
            
    def render(self):
        st.title("💬 AI Assistant Unisc - PPGSPI")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
            st.session_state.chatbot = AgentConversation(self.__azure_openai)
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if question := st.chat_input("Pergunte qualquer coisa!"):
            st.session_state.messages.append({"role": "user", "content": question})
            
            with st.chat_message("user"):
                st.markdown(question)
            
            result = st.session_state.chatbot.run(question)
            
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                assistant_response = result
                
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
if __name__ == "__main__":
    Chat().render()
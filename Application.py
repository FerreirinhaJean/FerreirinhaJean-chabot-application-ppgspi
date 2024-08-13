import streamlit as st
from UI.Chat import Chat

# chabot-application-ppgspi

class Application:
    
    def __init__(self) -> None:
        pass
    
    def render(self) -> None:
        st.markdown("""
            <style>
                .reportview-container {
                    margin-top: -2em;
                }
                #MainMenu {visibility: hidden;}
                .stDeployButton {display:none;}
                footer {visibility: hidden;}
                #stDecoration {display:none;}
            </style>
        """, unsafe_allow_html=True)
        Chat().render()
        
if __name__ == "__main__":
    Application().render()
        
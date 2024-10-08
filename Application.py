import streamlit as st
from UI.Login import Login

class Application:
    
    def __init__(self) -> None:
        self.__login = Login()
    
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
        self.__login.render()
        
if __name__ == "__main__":
    Application().render()
        
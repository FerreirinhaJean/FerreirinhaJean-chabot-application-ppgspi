import streamlit as st
import streamlit_authenticator as st_auth
import yaml
from yaml.loader import SafeLoader
from UI.Chat import Chat

class Login():
    
    def __init__(self) -> None:
        with open("config.yaml") as file:
            config = yaml.load(file, Loader=SafeLoader)
            
            self.username_admin = config["admin"]
            self.auth = st_auth.Authenticate(
                config["credentials"],
                config["cookie"]["name"],
                config["cookie"]["key"],
                config["cookie"]["expiry_days"]
            )
    
    def render(self) -> None:
        name, status_auth, user = self.auth.login(fields={"Username": "Usuário", "Password": "Senha", "Login": "Entrar"})
        
        if st.session_state["authentication_status"]:
            self.auth.logout(button_name="Sair", location="sidebar")
            st.markdown("""
                        <style>
                            section[data-testid="stSidebar"][aria-expanded="true"]{
                                display: none;
                            }
                        </style>
                        """, unsafe_allow_html=True
                        )
            st.empty()
            Chat().render()
        elif st.session_state["authentication_status"] is False:
            st.error("Usuário e/ou senha incorretos!")
        elif st.session_state["authentication_status"] is None:
            st.warning("Por favor entre com seu usuário e senha!")

if __name__ == "__main__":
    Login().render()
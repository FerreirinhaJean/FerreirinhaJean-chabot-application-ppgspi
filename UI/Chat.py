import streamlit as st
from chat.AgentConversation import AgentConversation
import os
from LLM.LLM import AzureOpenAI
import time
from db.MongoManager import MongoManager
import uuid


class Chat:

    def __init__(self) -> None:
        self.__azure_openai = AzureOpenAI(
            os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            os.getenv("AZURE_OPENAI_DEPLOYMENT_EMBEDDING"),
        )
        self.__mongo_db = MongoManager()
        self.__greeting_message = "Bem-vindo ao assistente virtual da Pós-Graduação em Processos e Sistemas Industriais da UNISC! Estou aqui para ajudar a esclarecer todas as suas dúvidas sobre o processo seletivo, conforme o edital do programa. Sinta-se à vontade para perguntar sobre inscrições, prazos, documentos necessários e qualquer outro detalhe que precise. Vamos começar?"

    def render(self):
        st.markdown(
            """
        <style>
               .block-container {
                    padding-top: 0rem;
                    margin-top: -3.5rem;
                    padding-bottom: 0rem;
                    padding-left: 4rem;
                    padding-right: 0rem;
                }
        </style>
        """,
            unsafe_allow_html=True,
        )
        st.title("💬 AI Assistant Unisc - PPGSPI")

        if "messages" not in st.session_state:
            st.session_state.messages = []
            st.session_state.messages.append(
                {"role": "assistant", "content": self.__greeting_message}
            )
            st.session_state.chatbot = AgentConversation(self.__azure_openai)
            st.session_state.id_conversation = str(uuid.uuid4())
            st.session_state.first_message = True

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

                if message["role"] == "assistant" and "source" in message:
                    for src in message["source"]:
                        with st.popover(src["title"]):
                            st.caption(src["content"])

        if question := st.chat_input("Pergunte sobre sua dúvida em relação ao processo seletivo do PPGSPI"):
            ## Caso não existe ainda o mesages ele recria
            if "messages" not in st.session_state:
                st.session_state.messages = []
                st.session_state.messages.append(
                    {"role": "assistant", "content": self.__greeting_message}
                )
                st.session_state.first_message = True
            if "chatbot" not in st.session_state:
                st.session_state.chatbot = AgentConversation(self.__azure_openai)
            if "id_conversation" not in st.session_state:
                st.session_state.id_conversation = str(uuid.uuid4())

            st.session_state.messages.append({"role": "user", "content": question})

            with st.chat_message("user"):
                st.markdown(question)

            result, source = st.session_state.chatbot.run(question)
            result = result.replace("`", "")
            result += f"\n___\n**Fontes:**\n\nDisponível em: [Mestrado em Sistemas e Processos Industriais - UNISC](https://www.unisc.br/pt/cursos/todos-os-cursos/mestrado-doutorado/mestrado/mestrado-em-sistemas-e-processos-industriais/informacoes-para-inscricao)"

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                assistant_response = result

                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)

                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(result)

                for src in source:
                    with st.popover(src["title"]):
                        st.caption(src["content"])

            st.session_state.messages.append(
                {"role": "assistant", "content": result, "source": source}
            )

            if st.session_state.first_message:
                self.__mongo_db.create_conversation(
                    st.session_state.messages, st.session_state.id_conversation
                )
                st.session_state.first_message = False
            else:
                self.__mongo_db.update_conversation(
                    st.session_state.messages, st.session_state.id_conversation
                )


if __name__ == "__main__":
    Chat().render()

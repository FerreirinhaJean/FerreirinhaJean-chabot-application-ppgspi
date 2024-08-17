from LLM.LLM import AzureOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains.question_answering import load_qa_chain
from .PromptTemplate import PROMPT_TEMPLATE
from .DefaultFallback import Fallback
from db.Db import Db

class AgentConversation():
    
    def __init__(self, azure_openai: AzureOpenAI, verbose: bool = True) -> None:
        self.__azure_openai = azure_openai
        self.__CHAIN_TYPE = "stuff"
        self.__verbose = verbose
        
        # self.__db = Db.load_vector("embbedings", self.__azure_openai.embedding)
        self.__db = Db().load_vector("embbedings/faiss_index", self.__azure_openai.embedding)
        self.__chain = self.__create_qa()
        
    def __create_qa(self) -> load_qa_chain:
        prompt_template = PromptTemplate(
            template=PROMPT_TEMPLATE,
            input_variables=["context", "chat_history", "question"]
        )
        
        memory_chat = ConversationBufferMemory(memory_key="chat_history", input_key="question")
        
        chain = load_qa_chain(
            llm=self.__azure_openai.llm,
            chain_type=self.__CHAIN_TYPE,
            memory=memory_chat,
            verbose=self.__verbose,
            prompt=prompt_template
        )
        
        return chain
    
    def run(self, question: str) -> tuple:
        context = self.__db.similarity_search(question, k=4)
        sources = ""
        for source in context:
            sources += f"- {source.metadata['source']}\n"
        
        sources += "\nDisponível em: [Mestrado em Sistemas e Processos Industriais - UNISC](https://www.unisc.br/pt/cursos/todos-os-cursos/mestrado-doutorado/mestrado/mestrado-em-sistemas-e-processos-industriais/informacoes-para-inscricao)"
        
        
        print(f"Documentos recuperados: {context}\n\n Origem do primeiro documento: {context[0].metadata['source']}")
        return self.__chain.run(input_documents=context, question=question), sources
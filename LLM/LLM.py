
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

class AzureOpenAI():

    def __init__(self, deployment_name, deployment_embedding_name, temperature: float = 0.0) -> None:
        self.__azure_deployment = deployment_name
        self.__temperature = temperature
        self.__api_version = "2024-05-01-preview"
        self.__embedding_name = deployment_embedding_name
        
        self.llm = self.__get_llm()
        self.embedding = self.__get_embedding()

    def __get_llm(self) -> AzureChatOpenAI:
        return AzureChatOpenAI(
            azure_deployment=self.__azure_deployment,
            temperature=self.__temperature,
            api_version=self.__api_version
        )
    
    def __get_embedding(self) -> AzureOpenAIEmbeddings:
        return AzureOpenAIEmbeddings(
            azure_deployment=self.__embedding_name,
            openai_api_version=self.__api_version
        )
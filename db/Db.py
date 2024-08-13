from langchain_community.vectorstores import FAISS

class Db():
    
    @staticmethod
    def load_vector(path: str, embedding: any):
        return FAISS.load_local(path, embedding, allow_dangerous_deserialization=True)
    
    @staticmethod
    def save_vector():
        pass
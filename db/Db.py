from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from documents.edital import edital

class Db():
    
    @staticmethod
    def load_vector(path: str, embedding: any):
        return FAISS.load_local(path, embedding, allow_dangerous_deserialization=True)
    
    @staticmethod
    def save_vector(embedding: any):
        documents = Db().__create_documents()
        vector_store = FAISS.from_documents(documents, embedding)
        vector_store.save_local("embbedings/faiss_index")
    
    @staticmethod
    def __create_documents() -> list[Document]:
        docs = []
        for section in edital:
            section_completed = f"{section['section']} - {section['section_name']}"
            pages_formatted = "Páginas: " if len(section['pages']) > 1 else "Página: "
            source_data = f"Seção {section_completed}. {pages_formatted}{', '.join(str(page) for page in section['pages'])}"
            
            page_content = f"{section_completed}\n{section['content']}"
            metadata = {"source": source_data}
            
            docs.append(Document(page_content=page_content, metadata=metadata))
        
        return docs
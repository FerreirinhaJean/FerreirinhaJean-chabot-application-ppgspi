from LLM.LLM import AzureOpenAI
import os
from db.Db import Db

azure_openai = AzureOpenAI(
    os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    os.getenv("AZURE_OPENAI_DEPLOYMENT_EMBEDDING")
)
Db.save_vector(azure_openai.embedding)
from pymongo import MongoClient
import os


class MongoManager:

    def __init__(self) -> None:
        uri = os.getenv("MONGO_URI")
        client = MongoClient(uri)
        print(f"URI: {uri}")
        self.__database = client.get_database(os.getenv("DATABASE"))
        self.__conversations_colletion = self.__database.get_collection("conversations")

    def create_conversation(self, messages: dict, id: str) -> None:
        try:
            _conversation = {"id_conversation": id, "messages": messages}
            self.__conversations_colletion.insert_one(_conversation)
        except:
            pass

    def update_conversation(self, messages: dict, id: str) -> None:
        try:
            query_filter = {"id_conversation": id}
            update_operation = {"$set": {"messages": messages}}
            self.__conversations_colletion.update_one(query_filter, update_operation)
        except:
            pass

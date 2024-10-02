from pymongo import MongoClient
import os
import logging


class MongoManager:

    def __init__(self) -> None:
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )

        uri = os.getenv("MONGO_URI")
        logging.info(f"URI: {uri}")
        logging.info(f'DATABASE: {os.getenv("DATABASE")}')

        client = MongoClient(uri)
        logging.info(client)
        self.__database = client.get_database(os.getenv("DATABASE"))
        self.__conversations_colletion = self.__database.get_collection("conversations")

    def create_conversation(self, messages: dict, id: str) -> None:
        try:
            _conversation = {"id_conversation": id, "messages": messages}
            self.__conversations_colletion.insert_one(_conversation)
        except Exception as ex:
            logging.error("Error to create conversation")
            logging.error(ex)

    def update_conversation(self, messages: dict, id: str) -> None:
        try:
            query_filter = {"id_conversation": id}
            update_operation = {"$set": {"messages": messages}}
            self.__conversations_colletion.update_one(query_filter, update_operation)
        except Exception as ex:
            logging.error("Error to update conversation")
            logging.error(ex)

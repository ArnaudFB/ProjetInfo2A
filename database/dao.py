from database.init_db import Database
from utils.singleton import Singleton
from abc import ABC, abstractmethod

class DAO(ABC):

    @abstractmethod
    def get_all(self) -> dict :
        pass

    @abstractmethod
    def add_new(self) -> bool :
        pass

   


import json
from abc import ABC, abstractmethod, abstractclassmethod


class AbstractBaseClassModel(ABC):
    def to_json(self):
        return json.dumps(vars(self)).encode(encoding="utf-8")

    def process_message(self, message):
        response = message.decode(encoding="utf-8")
        return json.loads(response)


class Message(AbstractBaseClassModel):
    def __init__(self, action, username=None, password=None, 
                 email=None, filename=None, tag=None, note_id=None):
        self.action = action
        self.username = username
        self.password = password
        self.email = email
        self.filename = filename
        self.tag = tag
        self.note_id = note_id

    @abstractmethod
    def to_json(self):
        return super().to_json()

    @abstractclassmethod
    def process_message(self, message):
        return super().process_message(message)


class Result(AbstractBaseClassModel):
    def __init__(self, success, note_id=None, 
                 author=None, filename=None, tag=None):
        self.success = success
        self.note_id = note_id
        self.author = author
        self.filename = filename
        self.tag = tag

    @abstractmethod
    def to_json(self):
        return super().to_json()

    @abstractclassmethod
    def process_message(self, message):
        return super().process_message(message)
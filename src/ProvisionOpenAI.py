import os

class ProvisionOpenAI:
    _api_key = None
    
    @classmethod
    def set_api_key(cls, api_key):
        if cls._api_key is None:
            cls._api_key = api_key
        else:
            raise Exception("OpenAI API key is already set")
    
    @classmethod
    def get_api_key(cls):
        if cls._api_key is None:
            raise Exception("OpenAI API key is not set")
        return cls._api_key
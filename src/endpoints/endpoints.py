import json
from typing import Optional

def read_json(path: str) -> dict:
    with open(path) as file:
        return json.load(file)
    
class Endpoints:
    def __init__(self):
        self.path = "src/endpoints/data.json"
        self.endpoints = read_json(self.path)

    def get(
            self, 
            resource: Optional[str] = None, 
            action: Optional[str] = None) -> dict:
        if action:
            for endpoint in self.endpoints:
                if endpoint.get("action") == action:
                    return endpoint
        elif resource:
            for endpoint in self.endpoints:
                if endpoint.get("resources") == resource:
                    return dict(endpoint)
        else:
            raise Exception("Não foi possível encontrar o endpoint")
            
    def get_all(self) -> list:
        return self.endpoints


from requests.adapters import HTTPAdapter
from typing import Union
from urllib3.util.retry import Retry
import requests

class Session:
    def __init__(self) -> None:
        
        self.session = requests.Session()
        self.retry =  Retry(
            connect = 1, 
            total = 5,
            backoff_factor = 0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=['GET','POST,PUT,DELETE']
        )

        self.adapter = HTTPAdapter(max_retries=self.retry)
        self.session.mount('http://', self.adapter)
        self.session.mount('https://', self.adapter)   
    
    def get(self) -> Union[requests.Session, None]:
        return self.session
    
class Api: 
    def __init__(
            self, 
            url: str, 
            headers: dict = None, 
            params: dict = None, 
            json: dict = None , 
            proxies: dict = None, 
    ) -> None:
        
        self.url = url,
        self.headers = headers,
        self.params = params, 
        self.json  = json, 
        self.verify = True,
        self.proxies = proxies,
        self.session = Session().get(),
        self.timeout = 30

    def get(self) -> Union[requests.Response, None]:
        response = self.session.get(
            url=self.url, 
            headers=self.headers, 
            params=self.params, 
            verify=self.verify, 
            proxies=self.proxies,
            timeout=self.timeout
            )
        return response
    
    def post(self) -> Union[requests.Response, None]:
        response = self.session.post(
            url=self.url, 
            headers=self.headers, 
            params=self.params, 
            json=self.json, 
            verify=self.verify, 
            proxies=self.proxies,
            timeout=self.timeout
            )
        return response
    
    def put(self) -> Union[requests.Response, None]:

        response = self.session.put(
            url=self.url, 
            headers=self.headers, 
            params=self.params, 
            json=self.json, 
            verify=self.verify, 
            proxies=self.proxies,
            timeout=self.timeout
            )

        return response
    
    def delete(self) -> Union[requests.Response, None]:
        response = self.session.delete(
            url=self.url, 
            headers=self.headers, 
            params=self.params, 
            json=self.json, 
            verify=self.verify, 
            proxies=self.proxies,
            timeout=self.timeout
            )
        return response
        
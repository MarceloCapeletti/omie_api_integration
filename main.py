from src.config import Settings
import json

import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy 

from src.api import Api

from src.endpoints import Endpoints

setting = Settings()

endpoints = Endpoints().get_all()

print(endpoints)
base_url = setting.BASE_URL
app_key = setting.APP_KEY
app_secret = setting.APP_SECRET

HEADERS = {
    'Content-Type': 'application/json'
}

def request(resource: str, body: dict, params:dict) -> dict:
    response = Api(
        url=f"{base_url}{resource}",
        params=params,
        json=body,
        headers=HEADERS).post(        
    )

    if response.status_code == 200:
        content = response.content
        json = response.json()
        return json
    
    else:

        raise Exception(f"Erro:`{response.status_code}")


def get_total_of_pages(resource:str, action:str, params:dict) -> int:
    payload = {

          "call": action,
          "app_key": app_key,
          "app_secret": app_secret,
          "param":[params]  

    }
    
    response = request(resource, payload, params)
    total_of_pages = response.get("total_de_paginas", 0)
    records = response.get("total_de_registros", 0)

    return total_of_pages

def save_to_file(resource: str, content: dict):
    content = json.dumps(content)
    file_name = resource.split("/")[-2]
    with open(f'{file_name}.json','w') as file:
        file.write(content)

def save_into_db(page:int, resource: str, df: pd.DataFrame , contents: str):
 
    connection_string = f'postgresql://{setting.DB_USERNAME}:{setting.DB_PASSWORD}@{setting.DB_HOST}:{setting.DB_PORT}/{'postgres'}'
    table_name = resource.split("/")[-2]

 
    engine = create_engine(connection_string)
    if page == 1:
        df.to_sql(table_name, engine, index=False, if_exists="append")
    else:
        df.to_sql(table_name, engine, index=False, if_exists="replace")

df = pd.DataFrame()

for endpoint in endpoints:
    print(endpoint)
    resource = endpoint.get("resources",None)

    action = endpoint.get("action", None)

    params = endpoint.get("params", None)

    data_source = endpoint.get("data_source", None)

    total_of_pages = get_total_of_pages(resource=resource, action=action, params=params)
    #print(total_of_pages)

    record_fetched = 0

    for page in range(1, 10):
        params["pagina"] = page

        body= {

          "call": action,
          "app_key": app_key,
          "app_secret": app_secret,
          "param":[params]  

             }

        response = request(resource, body, params)
        record_fetched += response.get("registros", 0)

        contents = response.get(data_source, [])

        black_list = ["tags", "recomendacoes", "homepage", "fax_ddd", "bloquear_exclusao", "produtor_rural"]

        for content in contents:
            for item in black_list:
                if item in content:
                    del content[item]

        #print(f"Page: {page},",f"Records:{record_fetched}")
        
       #print(contents)
  

        df1 = pd.json_normalize(contents)
        df = pd.concat([df, df1], ignore_index=True)
        print(df1)
    df.to_excel('clientes.xlsx')
    save_into_db(page, resource, df, contents)
    df = pd.DataFrame()




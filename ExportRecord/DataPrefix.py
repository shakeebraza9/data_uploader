from config import GOOGLE_SHEET_LINK
from config import PUBLIC_PATH
from config import slugify
import json
import os

import pandas as pd
class DataPrefix:

    @staticmethod
    def GenJSon():

        data = {}
        df_dict = pd.read_excel(GOOGLE_SHEET_LINK, sheet_name=None)

        for sheet_name, sheet_df in df_dict.items():
            cleaned = sheet_df.dropna(how="all")
            rows = cleaned.to_dict(orient="records")

            mapping = {}
            for row in rows:
                key = row.get("key")
                value = row.get("value")
                if key and value:
                    shetKey = str(key)
                    shetValue = str(value) 
                    mapping[shetKey.lower()] =  shetValue if shetValue != "nan" else None
            data[sheet_name] = mapping

            DataPrefix.createFile(sheet_name,mapping)

    

    @staticmethod
    def createFile(sheet_name,data):

        sheet_name = slugify(sheet_name)
        os.makedirs(PUBLIC_PATH  + "/json/", exist_ok=True)

        output_file =  PUBLIC_PATH  + "/json/" + sheet_name + " .json"
            # with open(PUBLIC_PATH+"/prople.csv",'w',newline='',encoding='utf-8') as file:
            # writer = csv.writer(file)
            # writer.writerows(csvData)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    
    @staticmethod
    def Bodydtype(value: str):
        return value
 
    @staticmethod
    def VehicleType( value: str):
        return value

    

    # @staticmethod
    # def FuleType(mapping,value):
    #     return value  

        
    # def TransmissionType(mapping,value):
    #     if not mapping or not value:
    #         return value  
    #     key = str(value).lower()
    #     return mapping.get(key, value)     

    # def SetMake(mapping,value):
    #     if not mapping or not value:
    #         return value  
    #     key = str(value).lower()
    #     return mapping.get(key, value)  

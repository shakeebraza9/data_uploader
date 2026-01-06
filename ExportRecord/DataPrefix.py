from config import GOOGLE_SHEET_LINK
from config import PUBLIC_PATH 
from config import slugify,getJSonPrefixFile
import json
import os,re

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

        output_file =  PUBLIC_PATH  + "/json/" + sheet_name + ".json"
            # with open(PUBLIC_PATH+"/prople.csv",'w',newline='',encoding='utf-8') as file:
            # writer = csv.writer(file)
            # writer.writerows(csvData)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    
    @staticmethod
    def Bodydtype(value: str):
        if not value:
            return value


        # try:
        reponse =getJSonPrefixFile("body-type")
        key = value.strip().lower()
        return reponse.get(key, value)

        # except Exception:
            # return value
 
    @staticmethod
    def VehicleType(value: str):
        if not value:
            return value

        reponse =getJSonPrefixFile("vehicle")
        key = value.strip().lower()
        return reponse.get(key, None)



    

    @staticmethod
    def FuleType(value: str):
        if not value:
            return value

        reponse =getJSonPrefixFile("fuel-type")
        key = value.strip().lower()
        return reponse.get(key, value)


    @staticmethod
    def TransmissionType(value: str):
        if not value:
            return value
        
        reponse =getJSonPrefixFile("transmission-type")
        key = value.strip().lower()
        return reponse.get(key, value)
    

 
    @staticmethod
    def SetMake(value:str):
        if not value:
            return value
        
        reponse =getJSonPrefixFile("make")
        key = value.strip().lower()
        return reponse.get(key, value)

    @staticmethod
    def SetModel(make: str, model: str, varient: str):
        if not model:
            return model
        body_map =getJSonPrefixFile("body-type")
        model_map =getJSonPrefixFile("model")
        key = model.strip().lower()
        
  
        try:
            # Remove Bodytype into model
            for body_type in body_map.keys():
                pattern = rf"\b{re.escape(body_type)}\b"
                key = re.sub(pattern, "", key, flags=re.IGNORECASE)

            key = re.sub(r"\s+", " ", key).strip()
            
            return model_map.get(key, key)

        except Exception:
            return model
        
        
    @staticmethod
    def SetVarient(make: str, model: str, varient: str):
        if not varient:
            return varient
        varient_map =getJSonPrefixFile("Variant")
        key = varient.strip().lower()
        
  
        try:
            return varient_map.get(key, key)

        except Exception:
            return varient
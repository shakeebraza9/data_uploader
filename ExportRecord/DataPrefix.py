from config import GOOGLE_SHEET_LINK
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
                    mapping[key.lower()] = value
            data[sheet_name] = mapping
        return data

    
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
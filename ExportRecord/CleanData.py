from config import PUBLIC_PATH 
from config import getJSonPrefixFile
import json
import os,re



class CleanData:

    @staticmethod
    def BcaClean(variant: str):
 
        if not variant:
            return variant

        # json_path = os.path.join(PUBLIC_PATH, "json", "webvariants.json")
        # if not os.path.exists(json_path):
        #     return variant

        # with open(json_path, "r", encoding="utf-8") as f:
        #     webvardata = json.load(f)

        # variant = re.sub(r"[^a-zA-Z0-9\s]", " ", variant)
        # variant = re.sub(r"\s+", " ", variant).strip()
        # words = variant.split(" ")
        # variant = " ".join(words[:3])
        
        return variant
        
        
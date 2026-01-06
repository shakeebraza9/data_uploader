import os
import pandas as pd
from CSVGenerator.FieldSet import FieldSet 
from datetime import datetime
import logging
from config import AUCTIONS_DIR,AUCTION_OUTPUT_DIR





def Main():

    os.makedirs(AUCTION_OUTPUT_DIR, exist_ok=True)

    for root, dirs, files in os.walk(AUCTIONS_DIR):
        final_csvs = [
            f for f in files
            if f.lower().endswith('.csv') and 'final' in f.lower() and f.lower() != 'final_barclay.csv'
        ]
        
        if final_csvs:
            parts = root.split(os.sep)
            if len(parts) >= 4:
                date_str = parts[-3] 
                current_year = datetime.now().year
                dt = datetime.strptime(f"{date_str} {current_year}", "%b %d %Y")
                formatted_date = dt.strftime("%d-%m-%Y")
                auction_house = parts[-2]
                

                folder_desc = parts[-1]
                chunks = folder_desc.split('-')
                if len(chunks) > 2 and chunks[1].isdigit():
                    folder_desc = f"{chunks[0]}-" + "-".join(chunks[2:])
                
                folder_name = f"{formatted_date}_{auction_house}_{folder_desc}"
                print(folder_name)
                
                for f in final_csvs:
                    src_path = os.path.join(root, f)
                    dst_path = os.path.join(AUCTION_OUTPUT_DIR, f"{folder_name}.csv")
                    

                  
                    
                    newData = []
                    df = pd.read_csv(src_path)
                    data = df.to_dict(orient="records") 
                    for key,value in enumerate(data):
                        newitem = FieldSet(value,auction_house)
                        newData.append(newitem)
                    
                    newcsv = pd.DataFrame(newData)
                    newcsv.to_csv(dst_path, index=False)
                
                    





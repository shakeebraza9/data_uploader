import os
import urllib3
import time
from datetime import datetime
from dotenv import load_dotenv
from CSVGenerator.Main import Main
from ExportRecord.Main import Main as ExportRecord

LOG_FILE = "auction_error.log"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()





# Main()
obj = ExportRecord()
obj.Run()

# if __name__ == "__main__":

#     folder_path = os.path.join(BASE_FOLDER, "final_csvs")
#     folder_path = folder_path.replace("/", "\\")
#     dataset = DataSet()
#     dataSet = dataset.data
#     auctions = Up.process_csvs_to_json(folder_path, dataSet)
  
#     # print(auctions)
#     LoginToken = Up.login_and_get_token() 



#     for auction in auctions:
#         platrfrom_id = Up.getPlatefromID(auction["platform"],LoginToken)
#         auction["platform_id"] = platrfrom_id
#         Up.post_or_update(auction, LoginToken)
#         time.sleep(3)   

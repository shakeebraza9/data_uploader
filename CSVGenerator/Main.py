import os
import pandas as pd
from CSVGenerator.FieldSet import FieldSet
from datetime import datetime
from config import AUCTIONS_DIR, AUCTION_OUTPUT_DIR

month = "12-Dec"

def Main():

    month_path = os.path.join(AUCTIONS_DIR, month)
    output_month_path = os.path.join(AUCTION_OUTPUT_DIR)

    os.makedirs(output_month_path, exist_ok=True)

    count = 0
    processed = set()  

    for root, dirs, files in os.walk(month_path):

        final_csvs = [
            f for f in files
            if f.lower().endswith(".csv")
            and "final" in f.lower()
            and f.lower() != "final_barclay.csv"
        ]

        if not final_csvs:
            continue

        parts = root.split(os.sep)
        if len(parts) < 4:
            continue

        date_str = parts[-3]   
        auction_house = parts[-2]  
        folder_desc = parts[-1]

        today = datetime.now()
        year = today.year

        try:
            dt = datetime.strptime(
                f"{month.split('-')[0]} {date_str} {year}",
                "%m %d %Y"
            )
        except:
            continue

        if dt.date() > today.date():
            dt = dt.replace(year=year - 1)

        formatted_date = dt.strftime("%d-%m-%Y")


        chunks = folder_desc.split("-")
        if len(chunks) > 2 and chunks[1].isdigit():
            folder_desc = f"{chunks[0]}-" + "-".join(chunks[2:])

        folder_name = f"{formatted_date}_{auction_house}_{folder_desc}"


        if folder_name in processed:
            continue

        dst_path = os.path.join(output_month_path, f"{folder_name}.csv")


        if os.path.exists(dst_path):
            print(f"⏭ Skipped (already exists): {folder_name}.csv")
            processed.add(folder_name)
            continue
        src_path = os.path.join(root, final_csvs[0])

        df = pd.read_csv(src_path)
        data = df.to_dict(orient="records")

        newData = [FieldSet(item, auction_house) for item in data]
        pd.DataFrame(newData).to_csv(dst_path, index=False)

        processed.add(folder_name)
        count += 1
        print(f"{count}. Created: {folder_name}.csv")

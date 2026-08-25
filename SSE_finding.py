from pymongo import MongoClient
import numpy as np
import pandas as pd
from datetime import datetime

client = MongoClient("mongodb+srv://jasonchow2312_db_user:BamDyafBx4pH6qbh@sse.saorkaw.mongodb.net/")
db = client["SSE_index_historical_data"]
collection = db["SSE_index"]


start_date_str = input("Enter start date (YYYY-MM-DD): ")
end_date_str = input("Enter end date (YYYY-MM-DD): ")


start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

# Query with datetime objects
query = {"Date": {"$gte": start_date, "$lte": end_date}}
results = collection.find(query)

print(f"Documents in date range {start_date_str} to {end_date_str}:")


for doc in results:
    print(doc)


docs_list = list(results) 
if docs_list:
    df = pd.DataFrame(docs_list)
    print("DataFrame preview:")
    print(df.head())
else:
    print("No documents found in the range.")
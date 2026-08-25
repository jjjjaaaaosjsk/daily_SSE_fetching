import requests
from pymongo import MongoClient
from datetime import datetime, timedelta
import yfinance as yf
import numpy as np
import pandas as pd


client = MongoClient("mongodb+srv://jasonchow2312_db_user:BamDyafBx4pH6qbh@sse.saorkaw.mongodb.net/")
db = client["SSE_index_historical_data"]
collection = db["SSE_index"]

record_update_date = datetime.now().date() - timedelta(days = 1)





with open('last_update_date.txt', 'r') as f:
    stored_date_str = f.read()
    stored_date = datetime.strptime(stored_date_str, '%Y-%m-%d').date()  
    print(f"last stored date: {stored_date}")
    
    
with open('last_update_date.txt', 'w') as f:
    f.write(str(record_update_date))
    print(f"Updated stored date to: {record_update_date}")
print(stored_date)

yesterday_date = datetime.now() - timedelta(days = 1)
ens_date = datetime.now()

ticker = '000001.SS'
SSE_data_yesterday = yf.download(ticker, start = stored_date, end = yesterday_date, interval = '1d')
refined = np.round(SSE_data_yesterday, 2)

refined.reset_index(inplace=True)
records = refined.to_dict('records')
refined.to_csv('SSE_datadaily.csv', index=False)


df = pd.read_csv('SSE_datadaily.csv')

# Clean the data: Remove rows with '000001.SS' (the ticker row)
df = df[~df.apply(lambda row: '000001.SS' in row.values, axis=1)]
df['Date'] = pd.to_datetime(df['Date'])

numeric_cols = ['Close', 'High', 'Low', 'Open', 'Volume']
df[numeric_cols] = df[numeric_cols].astype(float)


records = df.to_dict('records')

print(f"Records to insert: {len(records)}")
print("Sample record:", records[0] if records else "No records")

# Insert into MongoDB
if records:
    try:
        result = collection.insert_many(records)
        print(f"Inserted {len(result.inserted_ids)} documents.")
    except Exception as e:
        print(f"Insertion error: {e}")
else:
    print("No valid data to insert.")


print(f"Total documents in collection: {collection.count_documents({})}")
#collection.insert_many(records)




#df = refined.sort_index()
#df = df.reset_index()           # Date becomes a column
#df['Date'] = df['Date'].dt.date
#print(df.shape)
#print(df.to_dict())

#data_to_insert = refined.reset_index().to_dict('records')

#df.to_csv('SSE_dailydata.csv',index=False) 
 





#collection.insert_one({refined})

#for doc in collection.find({'Date': datetime(2010, 1, 4)}):
    #print(doc)

#print(datetime.now())
#stock_url = 
#def get_stock_info(stock_symbol):
#    response = requests.get(f"{stock_url}")
 #   print(f"code is {response.status_code}")
    
    




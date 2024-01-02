import os
import json
import datetime
import pandas as pd
from urllib.parse import quote
from dotenv import load_dotenv
from google.cloud import storage
from sqlalchemy import create_engine
load_dotenv()


bucket_name = 'tirumala-traders'
file_name = 'August1.json'

storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)
blob = bucket.blob(file_name)

# Download the file's content as a string
data_dict = blob.download_as_text()
data_dict = json.loads(data_dict)
data_lis = []

for each_dict in data_dict.get("data", {}).get("results", []):
    try:
        ref_date = each_dict["transactionDate"] / 1000
        fulfilment = each_dict["instrumentLevelSettlementDetails"].get("UPI_FULFILMENT", {}). \
            get("totalAmount", 0)
        if not fulfilment:
            fulfilment = each_dict["instrumentLevelSettlementDetails"].get("UPI_CC_FULFILMENT", {}). \
                get("totalAmount", 0)

        data_lis.append(
            {
                "transaction_id": each_dict["transactionId"],
                "transaction_timestamp": each_dict["transactionDate"],
                "transaction_date": datetime.datetime.fromtimestamp(ref_date).strftime("%Y-%m-%d"),
                "transaction_month": datetime.datetime.fromtimestamp(ref_date).strftime("%B"),
                "transaction_year": datetime.datetime.fromtimestamp(ref_date).strftime("%Y"),
                "payment_status": each_dict["paymentState"],
                "store_name": each_dict["merchantDetails"].get("storeName", None),
                "customer_name": each_dict["customerDetails"].get("userName", None),
                "customer_user_id": each_dict["customerDetails"].get("userId", None),
                "customer_mobile_number": each_dict["customerDetails"].get("phoneNumber", None),
                "payment_app": each_dict["paymentApp"]["paymentApp"],
                "amount": fulfilment,
                "settlement_date": datetime.datetime.fromtimestamp(each_dict.get("settlement",
                                                                                 {"settlementList": [{
                                                                                     "settlementDate":
                                                                                         each_dict[
                                                                                             "transactionDate"]}]})
                                                                   ["settlementList"][0][
                                                                       "settlementDate"] / 1000).strftime(
                    "%Y-%m-%d"),
                "settlement_amount": each_dict.get("settlement", {}).
                get("settlementList", [{"settlementAmount": 0}])[0]["settlementAmount"],
                "settlement_status": each_dict.get("settlement", {}).get("status", None)
            }
        )
    except Exception as e:
        print("************************************************************************************")
        print(str(e))
        print(each_dict)

print(data_lis)
df = pd.DataFrame(data_lis)
print(df)

print(os.environ)

host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
user = os.getenv("POSTGRES_USER")
db = os.getenv("POSTGRES_DB")
password = os.getenv("POSTGRES_PASSWORD")
print(host)
print(port)
print(user)
print(db)
print(password)
connection_string = f"postgresql+psycopg2://postgres:{quote(password.encode('utf-8'))}@{host}/{db}"
engine = create_engine(connection_string, echo=True)

connection = engine.connect()
res = df.to_sql(name="sales_dummy", con=connection, if_exists="append", index=False)
connection.commit()
connection.close()
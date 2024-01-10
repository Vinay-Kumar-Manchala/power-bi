import functions_framework
import os
import json
import datetime
import pandas as pd
from urllib.parse import quote
from google.cloud import storage
from sqlalchemy import create_engine


# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def hello_gcs(cloud_event):
    data = cloud_event.data
    try:

        storage_client = storage.Client()
        bucket_name = data['bucket']
        file_name = data['name']
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(file_name)
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
                print(str(e))

        df = pd.DataFrame(data_lis)
        host = os.getenv("POSTGRES_HOST")
        port = os.getenv("POSTGRES_PORT")
        user = os.getenv("POSTGRES_USER")
        db = os.getenv("POSTGRES_DB")
        password = os.getenv("POSTGRES_PASSWORD")

        connection_string = f"postgresql+psycopg2://{user}:{quote(password)}@{host}:{port}/{db}"
        engine = create_engine(connection_string, echo=True)
        connection = engine.connect()

        df.to_sql(name="sales", con=connection, if_exists="append", index=False)
        connection.commit()

    except Exception as e:
        print(str(e))

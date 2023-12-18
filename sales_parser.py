import os
import json
import datetime
import pandas as pd
from urllib.parse import quote
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("HOST")
port = os.getenv("PORT")
user = os.getenv("USER")
db = os.getenv("DB")
password = os.getenv("PASSWORD")

json_folders = os.listdir("D:\\my_projects\\Power BI\\Personal\\power-bi\\raw_data\\")
print(json_folders)
for each_folder in json_folders:
    data_lis = []
    json_file_path = os.listdir(f"D:\\my_projects\\Power BI\\Personal\\power-bi\\raw_data\\{each_folder}")
    for each_file in json_file_path:
        with open(f"D:\\my_projects\\Power BI\\Personal\\power-bi\\raw_data\\{each_folder}\\{each_file}", 'r') as json_file:
            data_dict = json.load(json_file)

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
    print(len(data_lis))
    df = pd.DataFrame(data_lis)

    connection_string = f"postgresql+psycopg2://postgres:{quote('PowerBI@123')}@34.93.100.255/tirumala_traders"
    engine = create_engine(connection_string, echo=True)

    connection = engine.connect()
    res = df.to_sql(name="sales", con=connection, if_exists="append", index=False)
    print(res)
    connection.commit()
    connection.close()

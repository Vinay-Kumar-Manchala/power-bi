We have a small business where we use a PhonePe QR scanner for online payments, and I visualized the data from their web with the following flow:

➡️Extract data from the merchant app via the Talend API and save it as JSON files. (The only manual step)
➡️Load the JSONs into Cloud Storage, triggering a Cloud Function.
➡️The function, equipped with a Python script, parses the files, structuring the data.
➡️Store the structured data in SQL, running in a Docker container on my Compute Engine.
➡️Visualize data using Power BI.

Tech Stack Used: PowerBI, Docker, SQL, GCP's Cloud Function, Cloud Storage & Compute Engine.

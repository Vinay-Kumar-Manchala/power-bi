import requests


url = "https://web-api.phonepe.com/apis/mi-web/v3/transactions/list"
params = {"offset": 0, "size": 100, "filters": {"status": ["COMPLETED"]}, "transactionType": "FORWARD",
          "from": 1698777000000, "to": 1701368999999, "selectedDateType": "custom"}
headers = {
    "sec-ch-ua": 'Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    "fingerprint": '2df947e64f72a3311ab3d2ede9c0b314_xrClI.2df947e64f72a3311ab3d2ede9c0b314_xrClI.2df947e64f72a3311ab3d2ede9c0b314_xrClI.2df947e64f72a3311ab3d2ede9c0b314_xrClI',
    "x-csrf-token": "tvVPb4WNGAm79gcsS9B7Wypvx4wn7Aab",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "x-forwarded-for": "14.98.12.178:443",
    "content-type": "application/json",
    "___internal-request-id": "445694e9-5429-48a1-8983-205d7f164ec7",
    "accept": "application/*",
    "sec-ch-ua-platform": 'Windows',
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cookie": "_ppabwduref=PAUREF2312121059253220066790; OCULUS_G_TOKEN=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; OCULUS_R_TOKEN=0416225a66d17188559336446a0c1c07; _ppabwdcid=ZXlKaGJHY2lPaUpJVXpVeE1pSjkuZXlKcGMzTWlPaUpRYUc5dVpWQmxSMkZ5Wm1sbGJHUWlMQ0pxZEdraU9pSTJNREJsWWpjMVl5MDVZalV4TFRReU4yUXRPR1U1TlMxa01ETXpNekF5Tnprek5EUWlMQ0pwWVhRaU9qRTJOekUyTURReU5ERXNJbTVpWmlJNk1UWTNNVFl3TkRFeU1Td2ljM1ZpSWpvaVFsVlRTVTVGVTFOZlYwVkNYMFJCVTBoQ1QwRlNSQ0lzSW5KdmJHVWlPaUpwYm1kbGMzUWlmUS5rdkcxQUJCNGJpcnVQSllRektFa1NYME9sUlBINVFDNW9tX2k5Mm9CNG9mV25vV0c4eFp3cTMwT1cxdEVCX3J5Zm4wTzhFVUd2MnE5VGlrMUxJaUw4Zw==; _ppabwdsid=dc6ffcd7-f990-482f-b8e5-621ce33a48be; _CKB2N1BHVZ=9K68hinxkg2umfxsWyO0oDGmledJDO9DjXhAzoaEfWBt2kPXXVrnWU5DiwuGzTmI; _X52F70K3N=zW3UUETjO0cQr9EK2ql5vMe7JuKMbYLn",
    "Fingerprint":
"2df947e64f72a3311ab3d2ede9c0b314_xrClI.2df947e64f72a3311ab3d2ede9c0b314_xrClI.2df947e64f72a3311ab3d2ede9c0b314_xrClI.2df947e64f72a3311ab3d2ede9c0b314_xrClI",
"Namespace": "insights",
"Origin": "https://business.phonepe.com",
"Referer": "https://business.phonepe.com/",
"Sec-Ch-Ua":'Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117',
"Sec-Ch-Ua-Mobile": "?0",
"Sec-Ch-Ua-Platform":"Windows",
"X-App-Id": "oculus",
"X-Csrf-Token": "zW3UUETjO0cQr9EK2ql5vMe7JuKMbYLn",
"X-Device-Fingerprint": "123",
"X-Source-Platform": "WEB",
"X-Source-Type": "WEB"
}
response = requests.post(url, params=params, headers=headers, allow_redirects=True)


if response.status_code == 200:
    print("Request successful")
    print("Response content:")
    print(response.text)
else:
    print(f"Request failed with status code {response.status_code}")

import requests

url = "https://www.knesset.gov.il/WebSiteApi/knessetapi/Votes/GetVoteDetails/39856"

headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "content-type": "application/json",
    "if-none-match": "W/\"340ee0d3-ff84-43dd-a3e8-d01efc29903f\"",
    "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "Referer": "https://main.knesset.gov.il/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.text)
else:
    print(f"Request failed with status code: {response.status_code}")



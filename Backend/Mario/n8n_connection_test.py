import requests


# ----------------- N8N HTTP Post Connection test ------------------------

url = "https://hackathonsabadell.app.n8n.cloud/webhook-test/89f9c18b-8d8c-47f9-8be8-5b9dcaece85a"


# JSON Message to send to n8n
payload = {
    "texto" : "hola"
}

#Headers for showing to the client the structure of the format
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)



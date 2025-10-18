import requests
import json

# ----------------- N8N HTTP Connector implementation ------------------------

url = "https://hackathonsabadell.app.n8n.cloud/webhook/89f9c18b-8d8c-47f9-8be8-5b9dcaece85a"

def request_models(input:str)->str:
    # JSON Message to send to n8n
    payload = {
        "texto" : input
    }

    #Headers for showing to the client the structure of the format
    headers = {
        "Content-Type": "application/json"
    }


    try:
        #Sending the request to the model
        response = requests.post(url, json=payload, headers=headers, timeout=30)

        # Check if it was successful
        response.raise_for_status()

        # Try to parse JSON response
        try:
            data = response.json()
            print("Data received from n8n:")
            print(json.dumps(data, indent=4))
        except ValueError:
            # If response is not JSON, print raw text
            print("An unexpected error occurred")
            print(response.text)

    except requests.exceptions.Timeout:
        print("The request timed out waiting for a response.")
    except requests.exceptions.RequestException as e:
        print(f"Error while sending request: {e}")



#Example of calling the function
#request_models("i want to send a bizum")
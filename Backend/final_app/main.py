from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_flow_with_n8n import n8n_connector as n8n

app = FastAPI()

# Agregar CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo para recibir el input
class InputData(BaseModel):
    input: str

@app.post("/predict")
def predict(data: InputData):
    #Received input from the frontend
    input_text = data.input
    input_text = "QUiero enviarle 1 millon de euros a un rey en africa"
    print(f"API WORKS - Received input: {input_text}")
    
    # check if audio in the future


    #Send text to the ai multimodel and wait for the response
    n8n_response = n8n.request_models(input_text)
    

    # Parsear la respuesta JSON a diccionario
    try:
        import json
        if isinstance(n8n_response, str):
            n8n_dict = json.loads(n8n_response)
        else:
            n8n_dict = n8n_response

        print(f"N8N Response parsed: {n8n_dict}")

    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error parsing N8N response: {e}")
        n8n_dict = {"error": "Failed to parse N8N response", "raw_response": str(n8n_response)}


    #Ver que caso es cada una
    if "path" in n8n_dict:
        return {
        "path": n8n_dict["path"],
        "Instructions for the users": n8n_dict["Instructions for the users"]
        }  
    else:
        return {
            "output": n8n_dict
        }

# Ejecutar con:
# uvicorn main:app --reload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Agregar CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/predict")
def predict(input):
    print("API WORKS")

    # si audio enviar a santi
    

    # enviar a n8n 
    n8n.request_models(input)

    

    return "hola"


#uvicorn main:app --reload
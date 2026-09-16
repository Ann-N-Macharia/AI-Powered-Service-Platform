# secure_triage_api.py - the triage service with the door locked
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from modules.auth import check_password, create_token, current_user
from modules.rate_limit import check_rate_limit
import os
import httpx
from  dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AfyaPlus Triage API (Secured)", version="1.1.0")

LLM_GATEWAY_URL = os.environ["LLM_GATEWAY_URL"]

class LoginRequest(BaseModel):
    username: str
    password: str

class TriageRequest(BaseModel):
    patient_message: str = Field(min_length=5, max_length=1000)
    county: str = Field(min_length=2, max_length=40)

@app.get("/health")
def health():
    return {"service": "triage-api", "version": "1.1.0", "status": "ok"}

@app.post("/token")
def login(body: LoginRequest):
    if not check_password(body.username, body.password):
        raise HTTPException(status_code=401, detail="Wrong username or password.")
    return {"access_token": create_token(body.username), "token_type": "bearer"}

@app.post("/triage")
def triage(request: TriageRequest, user: dict = Depends(current_user)):
    check_rate_limit(user["sub"])

    try:
        response = httpx.post(
            f"{LLM_GATEWAY_URL}/health-tip",
            json=
                {"patient_message": request.patient_message,
             "county": request.county
             },
            timeout=10.0,
        )
    except httpx.RequestError:
        raise HTTPException(503, "The model is unavailable. Please try again shortly.")

    if response.status_code == 503:
        raise HTTPException(503, "The model is unavailable. Please try again shortly.")
    if response.status_code >= 400:
        raise HTTPException(502, "Upstream error.")

    #append user
    result = response.json()
    result["handled_for"] = user["sub"]
    return result


  
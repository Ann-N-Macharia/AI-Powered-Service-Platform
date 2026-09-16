from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from modules.auth import current_user, create_token, check_password      # the very same module from Monday
from modules.agent_langchain import run_logistics_agent  # wraps Lab 2's agent
import uuid
import logging

logging.basicConfig(filename="mcp.log", level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("logistics")


app = FastAPI(title="AfyaPlus Logistics Agent API", version="1.0.0")

class AskRequest(BaseModel):
    question: str = Field(min_length=5, max_length=500)

class LoginRequest(BaseModel):
    username: str
    password: str


@app.get("/health")
def health():
    return {"service": "triage-api", "version": "1.1.0", "status": "ok"}

@app.post("/token")
def login(body: LoginRequest):
    if not check_password(body.username, body.password):
        raise HTTPException(status_code=401, detail="Wrong username or password.")
    return {"access_token": create_token(body.username), "token_type": "bearer"}

@app.post("/ask-logistics")
async def ask_logistics(body: AskRequest, user: dict = Depends(current_user)):
    trace_id = str(uuid.uuid4())[:8]
    logging.info("trace=%s user=%s question=%r", trace_id, user["sub"], body.question)
    answer = await run_logistics_agent(body.question)   # wraps Lab 2's agent
    return {"question": body.question, "answer": answer, "asked_by": user["sub"]}
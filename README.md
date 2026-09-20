 AfyaPlus Service Platform

## Overview
AfyaPlus is a Kenyan community-health operations platform that combines modern AI triage, secure API access, and logistics intelligence for clinics and county health teams. The domain is healthcare service delivery: patients submit symptoms, a protected FastAPI service classifies urgency, and staff can use an agent-backed MCP layer to check clinic stock, plan delivery routes, and estimate travel time between facilities. The platform is designed to be secure, observable, and easy to run locally or in Docker.

## Architecture
```text
Client / CLI / Browser
        |
        v
FastAPI service (secure triage API)
        |
        v
Docker / docker-compose runtime
        |
        v
MCP server (clinic and logistics tools)
        |
        v
Agent / LLM gateway
        |
        v
Agent API / health-tip orchestration
```

The core flow is: FastAPI service -> Docker -> MCP server -> agent -> agent API.

## Running the API
1. Create a local environment file and never commit it.
   ```bash
   cp "_1_Secure FastAPI Service/.env.example" "_1_Secure FastAPI Service/.env"
   ```
   Required keys include:
   - `OPENAI_API_KEY`
   - `MODEL_BASE_URL`
   - `LLM_GATEWAY_URL`
   - `JWT_SECRET`

   Keep `.env` on your machine only; do not commit it to Git.

2. Start the API from the service folder.
   ```bash
   cd "_1_Secure FastAPI Service"
   python -m venv .venv
   . .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   uvicorn servers.secure_triage_api:app --reload --host 0.0.0.0 --port 8000
   ```

3. Open the interactive documentation.
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

4. Obtain a JWT token.
   ```bash
   curl -X POST http://127.0.0.1:8000/token \
     -H "Content-Type: application/json" \
     -d '{"username":"username","password":"password"}'
   ```

   Expected response:
   ```json
   {
     "access_token": "<jwt>",
     "token_type": "bearer"
   }
   ```

5. Call the protected triage endpoint.
   ```bash
   curl -X POST http://127.0.0.1:8000/triage \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <JWT_TOKEN>" \
     -d '{
       "patient_message": "I have a sore throat that will not go away.",
       "county": "Nairobi"
     }'
   ```

   The endpoint validates both input size and bearer token. Invalid requests return `422` or `401` as appropriate.

## Running with Docker
1. Prepare the container environment file.
   ```bash
   cd "_2_Containerisation"
   cp .env.example .env
   ```

2. Build the image.
   ```bash
   docker build -t afyaplus-triage:1.0.0 -f images/Dockerfile.triage .
   ```

3. Run the container.
   ```bash
   docker run --rm -p 8000:8000 --env-file .env --name afyaplus-triage afyaplus-triage:1.0.0
   ```

   Expected startup output includes:
   ```text
   INFO:     Started server process [1]
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

4. Docker Compose flow (recommended for multi-service deployments):
   ```bash
   cd "_2_Containerisation"
   docker compose up --build
   ```

   Container image tags defined in the compose setup are:
   - `afyaplus-triage:1.0.0`
   - `afyaplus-agent:1.0.0`

## MCP Server & Agent
The MCP server exposes clinic and logistics tools that the agent can call as part of a multi-step workflow. The server lives under the `_3_MCP Server` folder and is built around a JSON clinic dataset and tools such as stock checks, route planning, and delivery ETA estimation.

1. Launch the MCP Inspector.
   ```bash
   cd "_3_MCP Server"
   npx @modelcontextprotocol/inspector
   ```
   Then connect the Inspector to the local MCP server and inspect the available tools/resources.

2. Available tool list.
   - `check_stock(item)`
   - `plan_delivery_route(start_clinic_id)`
   - `get_delivery_eta(from_clinic_id, to_clinic_id)`
   - `clinics://directory` resource

3. Run the agent client.
   ```bash
   cd "_4_Agent Integration"
   python client.py
   ```
   The client authenticates against the agent API and sends a logistics question using a bearer token.

4. Example question and expected behaviour.
   ```text
   Question: "Which clinic is running low on malaria kits and what is the best route from Kisumu Central?"
   ```
   Expected multi-tool behaviour:
   - the agent checks stock with `check_stock`
   - it reads the clinics directory or route metadata
   - it calls `plan_delivery_route` or `get_delivery_eta`
   - it returns a recommendation combining stock risk and travel planning

## Observability
Application and MCP logs are written locally to `mcp.log` in the working directory of the service or agent process. This is how the platform keeps traceability for each request.

To follow a single trace across logs:
```bash
# in the service directory
grep "trace=abcd1234" mcp.log
```

For Dockerized service logs, trace requests can also be followed with:
```bash
docker compose logs -f agent | grep trace=
docker compose logs -f triage | grep trace=
```

The agent API writes entries such as `trace=<id> user=<username> question=...`, which makes it easy to correlate a user question with MCP tool calls and downstream processing.

## Versioning & Contributing
- Contributing guide: [CONTRIBUTING.md](./CONTRIBUTING.md)
- Current service version tag: `1.1.0`
- Matching image tags used in the container setup: `afyaplus-triage:1.0.0` and `afyaplus-agent:1.0.0`

Use the version tag to track API changes and align deployment images with the documented release state.

# AI Powered Service Platform

This project is a multi-part service platform built around secure AI access, containerisation, and integration with an MCP server. It demonstrates a production-oriented approach to exposing AI capabilities through authenticated, validated, and deployable services.

## Project structure

- `_1_Secure FastAPI Service/` – secure API service with authentication, rate limiting, and validated request/response models
- `_2_Containerisation/` – Docker and docker-compose setup to run the service in containers
- `_3_MCP Server/` – model context protocol server and clinic/logistics data integration
- `_4_Agent Integration/` – integration layer for connecting AI agents to service components
- `_5_Engineering Report/` – engineering documentation and project reporting
- `project_delivery.md` – project delivery checklist and key requirements

## Core goals

- Build a secure FastAPI-based AI service
- Protect endpoints with JWT-based authentication
- Validate incoming data using Pydantic models
- Enforce request limits and service protection
- Package services using Docker containers
- Integrate with MCP-based tools and external data sources
- Document engineering decisions and deliverables

## Deliverable focus

The project aligns with the requirement to deliver:

- a protected AI endpoint with typed request/response models
- JWT login and authenticated access control
- a health endpoint for monitoring and probes
- validation and rejection of invalid or unauthorised requests
- containerised deployment support

## Typical workflow

1. Start the secure API service.
2. Authenticate via the login endpoint to receive a JWT token.
3. Send requests to protected routes using the token.
4. Validate responses and error handling for unauthenticated or invalid input.
5. Run the service in Docker for deployment-style testing.
6. Use the MCP server and agent integration for broader operational workflows.

## Tech stack

- Python
- FastAPI
- Pydantic
- JWT authentication
- Docker / Docker Compose
- MCP server integration

## Notes

This project is intended as a learning and delivery exercise for secure AI service design, deployment, and system integration.

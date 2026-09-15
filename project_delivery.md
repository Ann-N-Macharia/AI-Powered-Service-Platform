Deliverable 1: Secure FastAPI Service (25 marks)
An endpoint wrapping an AI model call, with typed Pydantic request and response models and field constraints
JWT authentication: a /token login endpoint, and protected routes returning 401 and 403 correctly
A /health endpoint reporting service name and version, left unprotected for probes
Demonstrated rejection of invalid input (422) and unauthenticated calls (401), with curl evidence
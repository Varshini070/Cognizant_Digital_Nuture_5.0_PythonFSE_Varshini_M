# Hands-on 8

Run `uvicorn main:app --reload`. The REST API is versioned under `/api/v1/`; its list endpoint returns a DRF-style offset pagination envelope and supports `search=`. All application errors use the documented `error` envelope.

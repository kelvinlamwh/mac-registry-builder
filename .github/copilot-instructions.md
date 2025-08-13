# Copilot Instructions for MAC Address Gatherer

## Overview
This project is a FastAPI-based service for gathering MAC addresses via ARP pings. It exposes a `/register` endpoint that triggers an ARP request to the client's IP address. The service is designed for local network discovery and device registration workflows.

## Architecture
- **Entrypoint:** `main.py` (root) launches the FastAPI app using Uvicorn with custom Loguru logging.
- **API Logic:** `src/main.py` defines the FastAPI app, the `/register` endpoint, and the ARP ping logic using Scapy.
- **Dependencies:** Managed via `pyproject.toml`. Key packages: `fastapi`, `uvicorn`, `loguru`, `scapy`.

## Key Patterns & Conventions
- **Logging:** Uses Loguru with a custom format. All logs are output to stderr. Adjust `LOGGER_ARGS` in `main.py` for log changes.
- **Network Operations:** ARP pings are performed with Scapy. The `_do_arp_ping` function is the main integration point for network discovery.
- **API Endpoints:** All endpoints are defined in `src/main.py`. The `/register` endpoint expects to be called from a client on the same network.
- **Python Version:** Requires Python 3.13+ (see `pyproject.toml`).

## Developer Workflows
- **Run the Service:**
  ```bash
  uv run main.py
  ```
  This starts the FastAPI app on port 5000.
- **Test the API:**
  Use `curl` or a browser to access `http://localhost:5000/register`.
- **Add Endpoints:**
  Define new endpoints in `src/main.py` and update the API logic as needed.
- **Dependency Management:**
  Add/remove packages in `pyproject.toml` and run `uv sync`.

## Integration Points
- **Scapy:** Used for low-level ARP operations. Ensure the service runs with sufficient privileges for raw socket operations.
- **Uvicorn:** Used as the ASGI server. Configured in `main.py`.

## Examples
- To add a new endpoint, follow the pattern in `src/main.py`:
  ```python
  @app.get("/new-endpoint")
  def new_endpoint():
      # ... logic ...
      return {"message": "New endpoint"}
  ```

## References
- Entrypoint: `main.py`
- API & ARP logic: `src/main.py`
- Dependencies: `pyproject.toml`
- Logging: `loguru` config in `main.py`

---
If any section is unclear or missing details, please provide feedback for further refinement.

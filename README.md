# MAC Address Gatherer API

A FastAPI-based service for gathering MAC addresses via ARP pings. This project is designed for local network discovery and device registration workflows.

## Caveats
- ARP ping may require elevated privileges (run with `sudo` if requied).
- [Npcap](https://npcap.com/) required on Windows
- **Local Network ONLY**: The service cannot reach beyond broadcast domain, and can only acknowledge machines within the same LAN segment.

## Getting Started

### 1. Install
```console
> uv sync
```

### 2. Run
```console
> uv run main.py
```

### 3. Use
Go `http://<IP Address>:5000/probe?key1=value1&key2=value2` on other machines, and see the console

### 4. Package
```console
> uvx pyinstaller mac_registry.spec
```

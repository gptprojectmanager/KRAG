
import requests
import json

def list_tools(server_name, server_port):
    """
    Elenca i tool disponibili su un server MCP.
    """
    url = f"http://{server_name}:{server_port}/tools"
    try:
        print(f"Richiesta tool a {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print(f"Tool trovati su {server_name}: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la comunicazione con il server MCP a {url}: {e}")

if __name__ == "__main__":
    list_tools("graphiti-mcp-server", 8000)
    list_tools("qdrant-mcp-server", 8001)

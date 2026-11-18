import json
import yaml
from pathlib import Path
from typing import Dict, List, Any

class OpenAPIParser:
    def __init__(self, spec_path: str):
        self.spec_path = Path(spec_path)
        self.spec_data = self._load_spec()

    def _load_spec(self) -> Dict[str, Any]:
        if not self.spec_path.exists():
            raise FileNotFoundError(f"El archivo de especificación {self.spec_path} no existe.")
        
        content = self.spec_path.read_text(encoding="utf-8")
        if self.spec_path.suffix in [".yaml", ".yml"]:
            return yaml.safe_load(content)
        elif self.spec_path.suffix == ".json":
            return json.loads(content)
        else:
            raise ValueError("Formato no soportado. Usa JSON o YAML.")

    def get_base_url(self) -> str:
        # Intenta extraer el servidor base de OpenAPI 3.x
        servers = self.spec_data.get("servers", [])
        if servers:
            return servers[0].get("url", "http://localhost:8000")
        return "http://localhost:8000"

    def extract_endpoints(self) -> List[Dict[str, Any]]:
        endpoints = []
        paths = self.spec_data.get("paths", {})
        
        for path, methods in paths.items():
            for method, details in methods.items():
                if method.lower() in ["get", "post", "put", "delete", "patch"]:
                    parameters = details.get("parameters", [])
                    endpoints.append({
                        "path": path,
                        "method": method.upper(),
                        "parameters": parameters,
                        "summary": details.get("summary", "")
                    })
        return endpoints
import httpx
import asyncio
from typing import Dict, List, Any
from rich.console import Console

console = Console()

class SecurityEngine:
    def __init__(self, base_url: str, headers: Dict[str, str] = None, verify_ssl: bool = False):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.verify_ssl = verify_ssl
        self.findings: List[Dict[str, Any]] = []

    async def scan_endpoint(self, client: httpx.AsyncClient, endpoint: Dict[str, Any]):
        path = endpoint["path"]
        method = endpoint["method"]
        
        # Simulación de pruebas basadas en heurísticas de rutas
        if "{id}" in path or "{user_id}" in path:
            await self._test_bola(client, path, method)
        
        await self._test_broken_auth(client, path, method)
        await self._test_excessive_data(client, path, method)

    async def _test_bola(self, client: httpx.AsyncClient, path: str, method: str):
        """API1: Broken Object Level Authorization (BOLA / IDOR)"""
        test_path = path.replace("{id}", "1").replace("{user_id}", "1")
        malicious_path = path.replace("{id}", "2").replace("{user_id}", "2")
        
        urls = [f"{self.base_url}{test_path}", f"{self.base_url}{malicious_path}"]
        for url in urls:
            try:
                response = await client.request(method, url, headers=self.headers, timeout=5.0)
                if response.status_code == 200:
                    self.findings.append({
                        "vulnerability": "API1: Broken Object Level Authorization (BOLA)",
                        "severity": "High",
                        "endpoint": url,
                        "method": method,
                        "status_code": response.status_code,
                        "detail": "El recurso respondió con éxito ante un cambio de ID sin validación aparente de sesión."
                    })
            except Exception as e:
                pass

    async def _test_broken_auth(self, client: httpx.AsyncClient, path: str, method: str):
        """API2: Broken Authentication"""
        url = f"{self.base_url}{path.replace('{id}', '1').replace('{user_id}', '1')}"
        try:
            # Petición sin cabeceras de autenticación
            response = await client.request(method, url, timeout=5.0)
            if response.status_code in [200, 201]:
                self.findings.append({
                    "vulnerability": "API2: Broken Authentication",
                    "severity": "Critical",
                    "endpoint": url,
                    "method": method,
                    "status_code": response.status_code,
                    "detail": "Endpoint protegido accesible sin token de autorización."
                })
        except Exception as e:
            pass

    async def _test_excessive_data(self, client: httpx.AsyncClient, path: str, method: str):
        """API3: Excessive Data Exposure"""
        if method == "GET":
            url = f"{self.base_url}{path.replace('{id}', '1').replace('{user_id}', '1')}"
            try:
                response = await client.request(method, url, headers=self.headers, timeout=5.0)
                if response.status_code == 200:
                    body_text = response.text.lower()
                    sensitive_keywords = ["password", "password_hash", "secret", "credit_card", "ssn"]
                    if any(kw in body_text for kw in sensitive_keywords):
                        self.findings.append({
                            "vulnerability": "API3: Excessive Data Exposure",
                            "severity": "Medium",
                            "endpoint": url,
                            "method": method,
                            "status_code": response.status_code,
                            "detail": "La respuesta JSON contiene palabras clave de datos sensibles (password/secret)."
                        })
            except Exception as e:
                pass

    async def run(self, endpoints: List[Dict[str, Any]]):
        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            tasks = [self.scan_endpoint(client, ep) for ep in endpoints]
            await asyncio.gather(*tasks)
        return self.findings
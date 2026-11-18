import asyncio
import click
from scanner.parser import OpenAPIParser
from scanner.engine import SecurityEngine
from scanner.reporter import Reporter

@click.command()
@click.option("--spec", required=True, help="Ruta al archivo OpenAPI/Swagger (JSON o YAML).")
@click.option("--url", default=None, help="URL base de la API (opcional si está en el spec).")
@click.option("--token", default=None, help="Token Bearer de autorización si se requiere.")
def main(spec, url, token):
    """Enterprise API Security Scanner CLI"""
    click.echo(f"[*] Analizando especificación: {spec}")
    
    parser = OpenAPIParser(spec)
    base_url = url or parser.get_base_url()
    endpoints = parser.extract_endpoints()
    
    click.echo(f"[*] URL Base detectada: {base_url}")
    click.echo(f"[*] Endpoints extraídos: {len(endpoints)}")

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    engine = SecurityEngine(base_url=base_url, headers=headers)
    
    click.echo("[*] Ejecutando pruebas de seguridad (OWASP API Top 10)...")
    findings = asyncio.run(engine.run(endpoints))

    reporter = Reporter(findings)
    reporter.print_cli_summary()
    reporter.save_reports()

if __name__ == "__main__":
    main()
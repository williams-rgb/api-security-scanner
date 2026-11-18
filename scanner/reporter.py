import json
from pathlib import Path
from jinja2 import Template
from rich.console import Console
from rich.table import Table

console = Console()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte de Seguridad - API Scanner</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f4f6f9; color: #333; }
        h1 { color: #d9534f; }
        .card { background: white; padding: 20px; margin-bottom: 15px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .High { border-left: 5px solid #f0ad4e; }
        .Critical { border-left: 5px solid #d9534f; }
        .Medium { border-left: 5px solid #5bc0de; }
    </style>
</head>
<body>
    <h1>Enterprise API Security Report</h1>
    <p>Total de hallazgos detectados: <strong>{{ findings | length }}</strong></p>
    {% for f in findings %}
    <div class="card {{ f.severity }}">
        <h3>{{ f.vulnerability }} [{{ f.severity }}]</h3>
        <p><strong>Endpoint:</strong> {{ f.method }} {{ f.endpoint }}</p>
        <p><strong>Código HTTP:</strong> {{ f.status_code }}</p>
        <p><strong>Detalle:</strong> {{ f.detail }}</p>
    </div>
    {% endfor %}
</body>
</html>
"""

class Reporter:
    def __init__(self, findings: list):
        self.findings = findings

    def print_cli_summary(self):
        table = Table(title="Resultados del Escaneo de Vulnerabilidades")
        table.add_column("Vulnerabilidad", style="bold red")
        table.add_column("Severidad", style="bold yellow")
        table.add_column("Método", style="cyan")
        table.add_column("Endpoint", style="green")

        for f in self.findings:
            table.add_row(f["vulnerability"], f["severity"], f["method"], f["endpoint"])
        
        console.print(table)

    def save_reports(self, json_path: str = "report.json", html_path: str = "report.html"):
        # Guardar JSON
        Path(json_path).write_text(json.dumps(self.findings, indent=4), encoding="utf-8")
        
        # Guardar HTML
        template = Template(HTML_TEMPLATE)
        html_content = template.render(findings=self.findings)
        Path(html_path).write_text(html_content, encoding="utf-8")
        console.print(f"[bold green][+] Reportes generados exitosamente: {json_path}, {html_path}[/bold green]")
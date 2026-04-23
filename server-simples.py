#!/usr/bin/env python3
"""Servidor simples para testar localmente"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
import sys
from pathlib import Path

# Importa as funções da API
sys.path.insert(0, str(Path(__file__).parent / 'api'))
try:
    from analisar import extrair_texto_pdf, analisar
    print('✓ API carregada com sucesso')
except ImportError as e:
    print(f'✗ Erro ao carregar API: {e}')
    sys.exit(1)

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Serve o frontend"""
        path = self.path
        if path == '/' or path == '':
            path = '/index.html'

        filepath = Path(__file__).parent / 'public' / path.lstrip('/')

        if filepath.exists() and filepath.is_file():
            with open(filepath, 'rb') as f:
                content = f.read()

            if str(filepath).endswith('.html'):
                mimetype = 'text/html'
            elif str(filepath).endswith('.css'):
                mimetype = 'text/css'
            elif str(filepath).endswith('.js'):
                mimetype = 'application/javascript'
            else:
                mimetype = 'text/plain'

            self.send_response(200)
            self.send_header('Content-type', mimetype)
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        """Processa análise de PDF"""
        if self.path == '/api/analisar':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)

                print(f'[API] Recebido PDF de {content_length} bytes')

                # Extrai texto
                texto = extrair_texto_pdf(body)
                print(f'[API] Texto extraído: {len(texto)} caracteres')

                if not texto.strip():
                    resposta = {'erro': 'Não foi possível extrair texto do PDF'}
                    self.send_json(400, resposta)
                    return

                # Analisa
                resultado = analisar(texto)
                print(f'[API] Análise concluída: {resultado["percentual"]}%')

                self.send_json(200, resultado)

            except Exception as e:
                print(f'[ERRO] {e}')
                self.send_json(500, {'erro': str(e)})
        else:
            self.send_response(404)
            self.end_headers()

    def send_json(self, status, data):
        """Envia resposta JSON"""
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        """CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        print(f'[{self.address_string()}] {format % args}')

if __name__ == '__main__':
    port = 8000
    server = HTTPServer(('127.0.0.1', port), Handler)
    print(f'\n🚀 Servidor em http://127.0.0.1:{port}')
    print(f'🛑 Ctrl+C para parar\n')
    server.serve_forever()

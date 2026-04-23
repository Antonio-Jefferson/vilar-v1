#!/usr/bin/env python3
"""
Servidor de desenvolvimento local para testar o Verificador SEDUC-MA
Executa: python3 dev-server.py
Acessa: http://localhost:8000
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import sys
from pathlib import Path

# Importa as funções da API
sys.path.insert(0, str(Path(__file__).parent / 'api'))
from analisar import extrair_texto_pdf, analisar, CHECKLIST

class DevHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Serve arquivos estáticos do frontend"""
        if self.path == '/' or self.path == '':
            self.path = '/index.html'

        file_path = Path(__file__).parent / 'public' / self.path.lstrip('/')

        if file_path.is_file():
            with open(file_path, 'rb') as f:
                content = f.read()

            # Define o tipo MIME
            if str(file_path).endswith('.html'):
                mime = 'text/html'
            elif str(file_path).endswith('.css'):
                mime = 'text/css'
            elif str(file_path).endswith('.js'):
                mime = 'application/javascript'
            elif str(file_path).endswith('.json'):
                mime = 'application/json'
            else:
                mime = 'application/octet-stream'

            self.send_response(200)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, 'Arquivo não encontrado')

    def do_POST(self):
        """Processa a análise de PDF"""
        if self.path == '/api/analisar':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)

                # Extrai texto do PDF
                paginas, erro = extrair_texto_pdf(body)

                if not paginas:
                    if erro:
                        msg = f'Erro ao extrair texto: {erro}'
                    else:
                        msg = 'PDF vazio ou sem texto extraível (pode ser um PDF com imagem/scanned). Certifique-se de usar um PDF com texto digital.'
                    self._responder(400, {'erro': msg})
                    return

                # Analisa o texto
                resultado = analisar(paginas)
                self._responder(200, resultado)

            except Exception as e:
                print(f"Erro: {e}")
                self._responder(500, {'erro': str(e)})
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        """Suporta CORS preflight"""
        self.send_response(200)
        self._cors()
        self.end_headers()

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _responder(self, status, dados):
        corpo = json.dumps(dados, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self._cors()
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def log_message(self, format, *args):
        print(f'[{self.address_string()}] {format % args}')

if __name__ == '__main__':
    # Verifica se PyMuPDF está instalado
    try:
        import fitz
        print('✓ PyMuPDF encontrado')
    except ImportError:
        try:
            import pypdf
            print('✓ PyPDF encontrado')
        except ImportError:
            print('⚠ Nenhuma biblioteca de PDF encontrada!')
            print('  Instale com: pip install pymupdf')
            sys.exit(1)

    host = '127.0.0.1'
    port = 8000
    server = HTTPServer((host, port), DevHandler)

    print(f'\n🚀 Servidor rodando em http://{host}:{port}')
    print(f'📂 Acesse: http://127.0.0.1:{port}')
    print(f'🛑 Pressione Ctrl+C para parar\n')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n✓ Servidor parado')

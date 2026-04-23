#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import unicodedata
import sys
from pathlib import Path

# Importa o checklist da API
sys.path.insert(0, str(Path(__file__).parent / 'api'))
from analisar import CHECKLIST, normalizar, verificar_item, extrair_texto_pdf, analisar

class APIHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/analisar':
            try:
                length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(length)

                # Extrai texto do PDF
                if body[:4] == b'%PDF':
                    texto, erro = extrair_texto_pdf(body)
                else:
                    texto = body.decode('utf-8', errors='ignore')
                    erro = None

                if not texto.strip():
                    if erro:
                        msg = f'Erro ao extrair texto: {erro}'
                    else:
                        msg = 'PDF vazio ou sem texto extraível (pode ser um PDF com imagem/scanned). Certifique-se de usar um PDF com texto digital.'
                    self._responder(400, {'erro': msg})
                    return

                resultado = analisar(texto)
                self._responder(200, resultado)

            except Exception as e:
                self._responder(500, {'erro': str(e)})
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS, GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _responder(self, status, dados):
        corpo = json.dumps(dados, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self._cors()
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def end_headers(self):
        self._cors()
        super().end_headers()

    def translate_path(self, path):
        # Se pedir /, serve public/index.html
        if path == '/':
            path = '/public/index.html'
        return super().translate_path(path)

    def log_message(self, format, *args):
        print(f'[{self.address_string()}] {format % args}')

if __name__ == '__main__':
    # Instala dependências se não existir
    try:
        import fitz
    except ImportError:
        print('📦 Instalando PyMuPDF...')
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pymupdf==1.24.5', '-q'])

    port = 8000
    server = HTTPServer(('127.0.0.1', port), APIHandler)
    print(f'🚀 Servidor rodando em http://127.0.0.1:{port}')
    print(f'📂 Abra no navegador: http://127.0.0.1:{port}')
    print(f'🛑 Pressione Ctrl+C para parar\n')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n✓ Servidor parado')

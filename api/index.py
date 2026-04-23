from http.server import BaseHTTPRequestHandler
import json
from analisar import extrair_texto_pdf, analisar

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/analisar':
            try:
                length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(length)

                texto, erro = extrair_texto_pdf(body)

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

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _responder(self, status, dados):
        corpo = json.dumps(dados, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self._cors()
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def log_message(self, *args):
        pass

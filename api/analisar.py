from http.server import BaseHTTPRequestHandler
import json
import unicodedata
import re

# ══════════════════════════════════════════════════════════════════
#  CHECKLIST DE DOCUMENTOS — EDITAL 29/2024 SEDUC-MA
# ══════════════════════════════════════════════════════════════════
CHECKLIST = [
    {
        "id": "diploma",
        "grupo": "Requisito Básico (BNCC)",
        "nome": "Diploma de Licenciatura / Bacharel ou Certidão de Conclusão",
        "icone": "🎓",
        "palavras": [
            ["licenciatura", "diploma"],
            ["licenciado em"],
            ["bacharel", "diploma"],
            ["certidao de conclusao"],
            ["conclusao de curso"],
            ["universidade", "curso de"],
        ],
    },
    {
        "id": "rg",
        "grupo": "Identificação",
        "nome": "Documento de Identificação (RG / CNH / Passaporte / CTPS)",
        "icone": "🪪",
        "palavras": [
            ["carteira de identidade"],
            ["registro geral"],
            ["carteira nacional de habilitacao"],
            ["passaporte"],
            ["carteira de trabalho"],
            ["ctps"],
            ["secretaria de seguranca publica"],
            ["instituto de identificacao"],
            ["delegacia geral de policia civil"],
        ],
    },
    {
        "id": "cpf",
        "grupo": "Dados Cadastrais",
        "nome": "CPF + comprovante de regularidade",
        "icone": "📄",
        "palavras": [
            ["comprovante de inscricao", "cpf"],
            ["comprovante de situacao cadastral"],
            ["receita federal", "cpf"],
            ["situacao cadastral", "regular"],
            ["ministerio da fazenda", "cpf"],
        ],
    },
    {
        "id": "pis_cnis",
        "grupo": "Dados Cadastrais",
        "nome": "Comprovante PIS/PASEP + E-Social ou CNIS",
        "icone": "📋",
        "palavras": [
            ["cnis"],
            ["cadastro nacional de informacoes sociais"],
            ["extrato previdenciario"],
            ["instituto nacional do seguro social"],
            ["inss", "nit"],
        ],
    },
    {
        "id": "titulo_eleitor",
        "grupo": "Dados Cadastrais",
        "nome": "Título de Eleitor + Certidão de Quitação Eleitoral",
        "icone": "🗳️",
        "palavras": [
            ["titulo eleitoral"],
            ["titulo de eleitor"],
            ["quitacao eleitoral"],
            ["tribunal superior eleitoral", "quite"],
            ["situacao inscricao", "regular"],
            ["justica eleitoral", "certidao"],
        ],
    },
    {
        "id": "banco",
        "grupo": "Dados Cadastrais",
        "nome": "Dados Bancários — BANCO DO BRASIL (obrigatório)",
        "icone": "🏦",
        "palavras": [
            ["banco do brasil"],
            ["conta salario", "banco do brasil"],
            ["extrato", "banco do brasil"],
        ],
    },
    {
        "id": "laudo_medico",
        "grupo": "Dados Cadastrais",
        "nome": "Laudo Médico de aptidão física e mental",
        "icone": "🏥",
        "palavras": [
            ["laudo medico"],
            ["aptidao fisica e mental"],
            ["atestado de saude"],
            ["perfeito estado de saude"],
            ["apto", "exercicio"],
            ["hospital", "atesto"],
        ],
    },
    {
        "id": "comprovante_residencia",
        "grupo": "Dados Cadastrais",
        "nome": "Comprovante de Residência",
        "icone": "🏠",
        "palavras": [
            ["comprovante de residencia"],
            ["conta de energia"],
            ["conta de luz"],
            ["fatura", "energia"],
            ["equatorial"],
            ["caema"],
            ["distribuidora de energia"],
            ["nota fiscal", "energia eletrica"],
        ],
    },
    {
        "id": "homologacao",
        "grupo": "Dados Cadastrais",
        "nome": "Homologação do Resultado Final (Diário Oficial)",
        "icone": "📰",
        "palavras": [
            ["diario oficial"],
            ["homologacao"],
            ["resultado final"],
            ["cadastro de reserva"],
            ["processo seletivo simplificado"],
            ["secretaria de estado da educacao", "edital"],
        ],
    },
    {
        "id": "carta_aceite",
        "grupo": "Dados Cadastrais",
        "nome": "Carta de Aceite — Regime de Integralidade (Anexo XVI)",
        "icone": "✉️",
        "palavras": [
            ["carta de aceite"],
            ["regime de integralidade"],
            ["tempo integral", "aceite"],
            ["anexo xvi"],
            ["modelo pedagogico", "aceite"],
        ],
    },
    {
        "id": "decl_penalidade",
        "grupo": "Declarações",
        "nome": "Declaração de não penalidade em função pública (Anexo XII)",
        "icone": "📝",
        "palavras": [
            ["nao ter sofrido", "penalidade"],
            ["penalidade incompativel"],
            ["nao sofri", "funcao publica"],
            ["investidura em funcao publica"],
            ["nao sofri em tempo algum"],
        ],
    },
    {
        "id": "decl_acumulacao",
        "grupo": "Declarações",
        "nome": "Declaração de não acumulação de cargo público",
        "icone": "📝",
        "palavras": [
            ["nao acumulacao"],
            ["acumulacao de cargo"],
            ["nao possuo vinculo empregaticio"],
            ["nao acumulo"],
            ["declaracao de nao acumulacao"],
        ],
    },
    {
        "id": "decl_bens",
        "grupo": "Declarações",
        "nome": "Declaração de Bens / Não possuir bens / Recibo IR (Anexo XIII/XIV/XV)",
        "icone": "📝",
        "palavras": [
            ["declaracao de bens"],
            ["nao possuir bens"],
            ["declaracao de nao possuir bens"],
            ["bens a declarar"],
            ["nao possuo bens"],
        ],
    },
    {
        "id": "cert_criminal_trf",
        "grupo": "Certidões Negativas",
        "nome": "Certidão Judicial Criminal Negativa — TRF 1ª Região",
        "icone": "⚖️",
        "palavras": [
            ["certidao judicial criminal negativa"],
            ["tribunal regional federal", "criminal"],
            ["processos de classes criminais"],
            ["trf", "criminal"],
        ],
    },
    {
        "id": "cert_eleitoral_trf",
        "grupo": "Certidões Negativas",
        "nome": "Certidão Judicial para Fins Eleitorais — TRF 1ª Região",
        "icone": "⚖️",
        "palavras": [
            ["certidao judicial para fins eleitorais"],
            ["tribunal regional federal", "eleitoral"],
            ["fins eleitorais", "trf"],
            ["inelegibilidade"],
        ],
    },
    {
        "id": "cert_tcu",
        "grupo": "Certidões Negativas",
        "nome": "Certidão Negativa de Contas Irregulares — TCU",
        "icone": "⚖️",
        "palavras": [
            ["tribunal de contas da uniao"],
            ["contas julgadas irregulares", "negativa"],
            ["cadirreg"],
            ["tcu", "certifica"],
        ],
    },
    {
        "id": "cert_tcu_eleitoral",
        "grupo": "Certidões Negativas",
        "nome": "Certidão Negativa de Contas Irregulares para Fins Eleitorais — TCU",
        "icone": "⚖️",
        "palavras": [
            ["contas julgadas irregulares para fins eleitorais"],
            ["responsaveis com contas julgadas irregulares para fins eleitorais"],
            ["tcu", "fins eleitorais"],
        ],
    },
    {
        "id": "cert_tcema",
        "grupo": "Certidões Negativas",
        "nome": "Certidão Negativa de Contas Irregulares — TCE-MA",
        "icone": "⚖️",
        "palavras": [
            ["tribunal de contas do estado do maranhao"],
            ["tcema"],
            ["contas julgadas irregulares", "maranhao"],
        ],
    },
    {
        "id": "cert_improbidade_1grau",
        "grupo": "Certidões Negativas",
        "nome": "Certidão Estadual 1º Grau — Improbidade Administrativa (TJMA)",
        "icone": "⚖️",
        "palavras": [
            ["improbidade administrativa", "primeiro grau"],
            ["improbidade administrativa", "1o grau"],
            ["improbidade administrativa", "1 grau"],
            ["tjma", "improbidade"],
        ],
    },
    {
        "id": "cert_improbidade_2grau",
        "grupo": "Certidões Negativas",
        "nome": "Certidão 2º Grau — Improbidade Administrativa (TJMA)",
        "icone": "⚖️",
        "palavras": [
            ["improbidade administrativa", "segundo grau"],
            ["improbidade administrativa", "2o grau"],
            ["distribuicao no segundo grau", "improbidade"],
        ],
    },
    {
        "id": "cert_penal_1grau",
        "grupo": "Certidões Negativas",
        "nome": "Certidão Estadual 1º Grau — Ações Penais (TJMA)",
        "icone": "⚖️",
        "palavras": [
            ["acoes penais", "primeiro grau"],
            ["acoes penais", "1o grau"],
            ["acoes penais", "1 grau"],
            ["tjma", "acoes penais", "primeiro"],
        ],
    },
    {
        "id": "cert_penal_2grau",
        "grupo": "Certidões Negativas",
        "nome": "Certidão 2º Grau — Ações Penais (TJMA)",
        "icone": "⚖️",
        "palavras": [
            ["acoes penais", "segundo grau"],
            ["acoes penais", "2o grau"],
            ["distribuicao no segundo grau", "acoes penais"],
        ],
    },
    {
        "id": "cert_antecedentes_ssp",
        "grupo": "Certidões Negativas",
        "nome": "Certidão de Antecedentes Criminais — Perícia Oficial MA (SSP-MA)",
        "icone": "⚖️",
        "palavras": [
            ["atestado de antecedentes criminais"],
            ["secretaria de estado da seguranca publica", "antecedentes"],
            ["instituto de identificacao", "maranhao"],
            ["ident/ma"],
            ["pericia oficial", "antecedentes"],
        ],
    },
    {
        "id": "cert_antecedentes_pf",
        "grupo": "Certidões Negativas",
        "nome": "Certidão de Antecedentes Criminais — Polícia Federal",
        "icone": "⚖️",
        "palavras": [
            ["policia federal", "antecedentes"],
            ["epol", "sinic"],
            ["sistema nacional de informacoes criminais"],
        ],
    },
    {
        "id": "cert_crimes_eleitorais_tse",
        "grupo": "Certidões Negativas",
        "nome": "Certidão de Crimes Eleitorais — TSE (tse.jus.br)",
        "icone": "🗳️",
        "palavras": [
            ["certidao de crimes eleitorais"],
            ["tribunal superior eleitoral", "condenacao criminal eleitoral"],
            ["nao constar registro de condenacao criminal eleitoral"],
            ["tse", "crimes eleitorais"],
            ["crimes eleitorais", "transitada em julgado"],
        ],
    },
]


def normalizar(texto: str) -> str:
    nfkd = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in nfkd if not unicodedata.combining(c))
    return sem_acento.lower()


def verificar_item(texto_norm: str, palavras_grupos: list) -> bool:
    for grupo in palavras_grupos:
        if all(normalizar(p) in texto_norm for p in grupo):
            return True
    return False


def extrair_texto_pdf(conteudo_bytes: bytes) -> str:
    try:
        import fitz
        doc = fitz.open(stream=conteudo_bytes, filetype="pdf")
        partes = []
        for pagina in doc:
            partes.append(pagina.get_text())
        doc.close()
        return "\n".join(partes)
    except ImportError:
        try:
            import pypdf
            reader = pypdf.PdfReader(stream=conteudo_bytes)
            partes = []
            for page in reader.pages:
                partes.append(page.extract_text())
            return "\n".join(partes)
        except:
            return ""
    except Exception as e:
        return ""


def analisar(texto: str) -> dict:
    texto_norm = normalizar(texto)
    encontrados = []
    faltando = []

    for item in CHECKLIST:
        achado = verificar_item(texto_norm, item["palavras"])
        registro = {
            "id": item["id"],
            "grupo": item["grupo"],
            "nome": item["nome"],
            "icone": item["icone"],
        }
        if achado:
            encontrados.append(registro)
        else:
            faltando.append(registro)

    return {
        "total": len(CHECKLIST),
        "encontrados": encontrados,
        "faltando": faltando,
        "percentual": round(len(encontrados) / len(CHECKLIST) * 100),
    }


class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)

            content_type = self.headers.get("Content-Type", "")

            if "application/pdf" in content_type or body[:4] == b"%PDF":
                texto = extrair_texto_pdf(body)
            else:
                # tenta decodificar como texto
                texto = body.decode("utf-8", errors="ignore")

            if not texto.strip():
                self._responder(400, {"erro": "Não foi possível extrair texto do PDF."})
                return

            resultado = analisar(texto)
            self._responder(200, resultado)

        except Exception as e:
            self._responder(500, {"erro": str(e)})

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _responder(self, status: int, dados: dict):
        corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def log_message(self, *args):
        pass

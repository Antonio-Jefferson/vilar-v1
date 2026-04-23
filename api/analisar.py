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
            ["diploma de graduacao"],
            ["certificado de conclusao"],
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
            ["cnh"],
            ["passaporte"],
            ["carteira de trabalho"],
            ["ctps"],
            ["secretaria de seguranca publica"],
            ["instituto de identificacao"],
            ["delegacia geral de policia civil"],
            ["documento de identidade"],
            ["rg numero"],
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
            ["cpf", "inscrito"],
            ["numero do cpf"],
            ["cadastro de pessoa fisica"],
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
            ["pis", "pasep"],
            ["e-social"],
            ["numero de inscricao social"],
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
            ["eleitor", "numero do titulo"],
            ["certidao de quitacao"],
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
            ["bb", "conta corrente"],
            ["agencia", "banco do brasil"],
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
            ["medico responsavel"],
            ["apto para exercer"],
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
            ["agua e esgoto"],
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


def verificar_item(texto_norm: str, palavras_grupos: list) -> tuple[bool, int]:
    max_score = 0
    encontrado = False

    for grupo in palavras_grupos:
        if all(normalizar(p) in texto_norm for p in grupo):
            encontrado = True
            score = min(100, 50 + (len(grupo) * 15))
            max_score = max(max_score, score)

    if encontrado:
        return True, max_score

    for grupo in palavras_grupos:
        matches = sum(1 for p in grupo if normalizar(p) in texto_norm)
        if matches > 0:
            score = int((matches / len(grupo)) * 70)
            max_score = max(max_score, score)

    if max_score > 0:
        return False, max_score

    return False, 0


def processar_imagem_ocr(imagem_pil):
    """Pipeline completo de pré-processamento para OCR de imagens escaneadas"""
    try:
        import cv2
        import numpy as np
        from PIL import Image

        img = cv2.cvtColor(np.array(imagem_pil), cv2.COLOR_RGB2BGR)

        # 1. Upscaling se imagem pequena
        altura, largura = img.shape[:2]
        if altura < 1000 or largura < 1000:
            escala = max(1000 / altura, 1000 / largura)
            img = cv2.resize(img, None, fx=escala, fy=escala, interpolation=cv2.INTER_CUBIC)

        # 2. Converter para escala de cinza
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 3. Denoising (remover ruído mantendo bordas)
        denoised = cv2.fastNlMeansDenoising(gray, h=10, templateWindowSize=7, searchWindowSize=21)

        # 4. Remover sombras e melhorar contraste com CLAHE
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(10, 10))
        enhanced = clahe.apply(denoised)

        # 5. Binarização automática com Otsu
        _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # 6. Remover bordas escuras (margens)
        height, width = binary.shape
        crop_top = int(height * 0.02)
        crop_bottom = int(height * 0.02)
        crop_left = int(width * 0.02)
        crop_right = int(width * 0.02)
        binary = binary[crop_top:height-crop_bottom, crop_left:width-crop_right]

        # 7. Operações morfológicas para limpar
        kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))

        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel_close)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_open)

        # 8. Corrigir skew (inclinação) do documento
        binary = corrigir_inclinacao(binary)

        # 9. Inverter cores se necessário (preto em branco)
        if np.mean(binary) < 127:
            binary = cv2.bitwise_not(binary)

        return Image.fromarray(binary)

    except Exception as e:
        print(f"Erro no processamento: {e}")
        return imagem_pil


def corrigir_inclinacao(imagem):
    """Corrige a inclinação/rotação da imagem escaneada"""
    try:
        import cv2
        import numpy as np

        coords = np.column_stack(np.where(imagem > 200))
        if len(coords) < 10:
            return imagem

        angle = cv2.minAreaRect(coords)[2]
        if angle < -45:
            angle = 90 + angle

        if abs(angle) > 0.5:
            h, w = imagem.shape
            matriz_rotacao = cv2.getRotationMatrix2D((w/2, h/2), angle, 1.0)
            imagem = cv2.warpAffine(imagem, matriz_rotacao, (w, h),
                                   borderMode=cv2.BORDER_REPLICATE,
                                   flags=cv2.INTER_CUBIC)

        return imagem
    except:
        return imagem


def extrair_texto_pdf(conteudo_bytes: bytes) -> tuple[list, str]:
    """Extrai texto página por página, retorna lista de (texto, número_página)"""
    try:
        import fitz
        doc = fitz.open(stream=conteudo_bytes, filetype="pdf")
        paginas = []
        for idx, pagina in enumerate(doc, 1):
            texto = pagina.get_text()
            if texto.strip():
                paginas.append((texto, idx))
        doc.close()
        if paginas:
            return paginas, None
    except ImportError as e:
        pass
    except Exception as e:
        pass

    try:
        import pypdf
        reader = pypdf.PdfReader(stream=conteudo_bytes)
        paginas = []
        for idx, page in enumerate(reader.pages, 1):
            texto = page.extract_text()
            if texto.strip():
                paginas.append((texto, idx))
        if paginas:
            return paginas, None
    except Exception as e:
        pass

    try:
        import pdf2image
        import pytesseract

        images = pdf2image.convert_from_bytes(conteudo_bytes, dpi=300)
        paginas = []
        for idx, img in enumerate(images, 1):
            img_processada = processar_imagem_ocr(img)
            texto_ocr = pytesseract.image_to_string(img_processada, lang='por', config='--psm 3')
            if texto_ocr.strip():
                paginas.append((texto_ocr, idx))
        if paginas:
            return paginas, None
        return [], "OCR não encontrou texto no PDF (tente melhorar a qualidade da imagem)"
    except ImportError:
        return [], "Instale: pip install pdf2image pytesseract. Também instale tesseract-ocr: apt-get install tesseract-ocr"
    except Exception as e:
        return [], f"OCR error: {str(e)}"


def analisar(paginas_texto: list) -> dict:
    """Analisa páginas de texto retornando documentos encontrados com páginas"""
    encontrados = []
    faltando = []
    incertos = []

    for item in CHECKLIST:
        melhor_score = 0
        pagina_encontrada = None

        for texto, num_pagina in paginas_texto:
            texto_norm = normalizar(texto)
            achado, score = verificar_item(texto_norm, item["palavras"])

            if score > melhor_score:
                melhor_score = score
                if score > 0:
                    pagina_encontrada = num_pagina

        registro = {
            "id": item["id"],
            "grupo": item["grupo"],
            "nome": item["nome"],
            "icone": item["icone"],
            "score": melhor_score,
        }

        if pagina_encontrada:
            registro["pagina"] = pagina_encontrada

        if melhor_score >= 70:
            encontrados.append(registro)
        elif melhor_score >= 30 and melhor_score < 70:
            incertos.append(registro)
        else:
            faltando.append(registro)

    total_encontrados = len(encontrados)
    total_incertos = len(incertos)
    total_faltando = len(faltando)
    total = len(CHECKLIST)

    percentual = round(total_encontrados / total * 100)

    aviso = None
    if total_incertos > 0:
        aviso = f"⚠️ {total_incertos} documento(s) com confiança baixa - revisar manualmente"

    return {
        "total": total,
        "encontrados": encontrados,
        "incertos": incertos,
        "faltando": faltando,
        "percentual": percentual,
        "aviso": aviso,
    }

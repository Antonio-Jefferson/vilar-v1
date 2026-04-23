# Deploy na Vercel

## Pré-requisitos
- Conta na [Vercel](https://vercel.com)
- Git instalado e repositório configurado

## Passos para Deploy

### 1. Preparar repositório
```bash
git add -A
git commit -m "Preparar para deploy na Vercel"
git push origin main
```

### 2. Conectar no Vercel
- Acesse https://vercel.com/new
- Selecione seu repositório GitHub
- Vercel detectará automaticamente a configuração Python
- Clique em "Deploy"

### 3. Esperar o build
O Vercel vai:
- Instalar dependências do `requirements.txt`
- Compilar a API serverless
- Fazer deploy do frontend estático

## ⚠️ Nota Importante: OCR (Tesseract)

**Tesseract OCR não está disponível no Vercel** por padrão.

**Duas soluções:**

### Opção 1: Usar apenas PDFs com texto digital (Recomendado)
- A aplicação funcionará perfeitamente para PDFs normais
- Para PDFs scanned, use uma ferramenta de OCR separada antes de fazer upload

### Opção 2: Usar API de OCR externo
- Use serviços como:
  - Google Cloud Vision API
  - AWS Textract
  - OCR.space API

## Estrutura de Arquivos

```
/api/
  ├── index.py          # Handler serverless (Vercel chama isso)
  └── analisar.py       # Lógica de análise
/public/
  └── index.html        # Frontend
vercel.json            # Configuração Vercel
requirements.txt       # Dependências Python
```

## Testando Localmente

```bash
# Ativar venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Rodar servidor dev
python3 dev-server.py
```

Acesse: http://127.0.0.1:8000/

## Endpoints

**POST** `/api/analisar`
- Body: PDF em bytes
- Content-Type: `application/pdf`
- Response: JSON com análise

## Variáveis de Ambiente

Se usar OCR cloud API no futuro:
```bash
# Na Vercel, adicione em Settings > Environment Variables
OCR_API_KEY=sua_chave_aqui
```

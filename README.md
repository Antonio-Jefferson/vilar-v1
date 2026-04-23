# Verificador de Documentos — Edital 29/2024 SEDUC-MA

Site para verificar documentação do processo seletivo simplificado da SEDUC-MA.
**Análise 100% por palavras-chave, sem IA, sem envio de dados a terceiros.**

---

## 📁 Estrutura

```
edital29-site/
├── api/
│   └── analisar.py       ← API Python (Vercel Serverless)
├── public/
│   └── index.html        ← Frontend
├── requirements.txt      ← Dependências Python
└── vercel.json           ← Configuração Vercel
```

---

## 🚀 Como publicar na Vercel (passo a passo)

### 1. Crie uma conta gratuita
Acesse https://vercel.com e crie uma conta (pode usar o Google).

### 2. Instale o Git e crie um repositório
- Baixe o Git: https://git-scm.com
- Crie uma conta no GitHub: https://github.com
- Crie um repositório novo chamado `verificador-seduc`

### 3. Suba os arquivos para o GitHub
```bash
git init
git add .
git commit -m "primeiro envio"
git remote add origin https://github.com/SEU_USUARIO/verificador-seduc.git
git push -u origin main
```

### 4. Conecte à Vercel
1. Acesse https://vercel.com/new
2. Clique em "Import Git Repository"
3. Selecione o repositório `verificador-seduc`
4. Clique em **Deploy**

Pronto! Em ~2 minutos o site estará no ar com uma URL do tipo:
`https://verificador-seduc.vercel.app`

---

## ⚙️ Como funciona

1. O usuário faz upload do PDF no site
2. O frontend envia o PDF para `/api/analisar`
3. A API Python extrai o texto com PyMuPDF
4. Busca por palavras-chave de cada um dos 24 documentos obrigatórios
5. Retorna JSON com encontrados e faltando
6. O frontend exibe o checklist visual

---

## 📋 Documentos verificados (25 itens)

- Diploma / Certidão de Conclusão
- RG / CNH / Documento de identificação
- CPF + regularidade
- PIS/CNIS
- Título de Eleitor + Quitação Eleitoral
- Dados bancários (Banco do Brasil)
- Laudo Médico
- Comprovante de Residência
- Homologação no Diário Oficial
- Carta de Aceite (Anexo XVI)
- Declaração de não penalidade (Anexo XII)
- Declaração de não acumulação
- Declaração de bens (Anexo XIII/XIV/XV)
- Certidão Criminal TRF 1ª Região
- Certidão Eleitoral TRF 1ª Região
- Certidão TCU
- Certidão TCU Fins Eleitorais
- Certidão TCE-MA
- Certidão Improbidade 1º Grau TJMA
- Certidão Improbidade 2º Grau TJMA
- Certidão Ações Penais 1º Grau TJMA
- Certidão Ações Penais 2º Grau TJMA
- Antecedentes Criminais SSP-MA
- Antecedentes Criminais Polícia Federal
- **Certidão de Crimes Eleitorais — TSE** *(novo)*

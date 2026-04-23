#!/bin/bash

cd "$(dirname "$0")"

echo "🚀 Iniciando servidor na porta 8000..."
echo "📂 Acesse: http://127.0.0.1:8000"
echo "🛑 Pressione Ctrl+C para parar"
echo ""

cd public && python3 -m http.server 8000

#!/bin/bash
# Aguarda o CSV do gerador e o PostgreSQL ficarem disponíveis antes de rodar a análise.

CSV_FILE="${ARQUIVO_DADOS_BRUTOS:-/data/dados_ist_realistas.csv}"
DB_HOST="${DB_HOST:-postgres}"
DB_PORT="${DB_PORT:-5432}"

csv_pronto()      { [ -f "$CSV_FILE" ]; }
postgres_pronto() { pg_isready -h "$DB_HOST" -p "$DB_PORT" -q; }

echo "Aguardando o arquivo CSV ($CSV_FILE) e o PostgreSQL em $DB_HOST:$DB_PORT ficarem prontos..."

until csv_pronto && postgres_pronto; do
  csv_pronto      || echo "  - CSV não encontrado, aguardando..."
  postgres_pronto || echo "  - PostgreSQL não está pronto, aguardando..."
  sleep 2
done

echo "Arquivo CSV encontrado e PostgreSQL pronto. Rodando análise com R..."
exec Rscript R/main.R

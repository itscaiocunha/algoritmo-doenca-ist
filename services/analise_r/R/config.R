# Configuração da etapa de análise/tratamento.
# Os valores podem ser sobrescritos por variáveis de ambiente (definidas no docker-compose).

config <- list(
  arquivo_entrada = Sys.getenv("ARQUIVO_DADOS_BRUTOS", "/data/dados_ist_realistas.csv"),
  arquivo_saida   = Sys.getenv("ARQUIVO_DADOS_TRATADOS", "/data/dados_ist_tratados.csv"),

  db = list(
    host     = Sys.getenv("DB_HOST", "postgres"),
    port     = as.integer(Sys.getenv("DB_PORT", "5432")),
    name     = Sys.getenv("POSTGRES_DB", "ist_db"),
    user     = Sys.getenv("POSTGRES_USER", "admin_ist"),
    password = Sys.getenv("POSTGRES_PASSWORD", "istunifeob"),
    tabela   = "dados_ist_tratados"
  )
)

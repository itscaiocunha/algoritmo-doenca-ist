# Exportação dos dados tratados (CSV para o Spark e PostgreSQL para o Grafana).

library(RPostgreSQL)
library(DBI)

exportar_csv <- function(dados, caminho) {
  write.csv(dados, caminho, row.names = FALSE)
}

# Falhas de conexão são registradas no log, mas não interrompem o pipeline.
exportar_postgres <- function(dados, db) {
  con <- NULL

  tryCatch({
    con <- DBI::dbConnect(RPostgreSQL::PostgreSQL(),
                          host = db$host,
                          port = db$port,
                          dbname = db$name,
                          user = db$user,
                          password = db$password)

    print(paste("\nConectado com sucesso ao banco de dados PostgreSQL:", db$name))

    dbWriteTable(con, db$tabela, dados, row.names = FALSE, overwrite = TRUE)

    print(paste("Dados tratados exportados com sucesso para a tabela '", db$tabela, "' no PostgreSQL.", sep = ""))

  }, error = function(e) {
    print(paste("\nErro ao conectar ou exportar para o PostgreSQL:", e$message))
  }, finally = {
    if (!is.null(con)) {
      DBI::dbDisconnect(con)
      print("Desconectado do banco de dados PostgreSQL.")
    }
  })
}

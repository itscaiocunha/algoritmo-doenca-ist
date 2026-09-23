# Tratamento dos dados: imputação, conversão de tipos e padronização de categorias.
# Cada função recebe e devolve o data.frame completo.

# --- Dados Numéricos ---

imputar_renda_mediana <- function(dados) {
  print(colSums(is.na(dados)))

  mediana_renda <- median(dados$renda_media, na.rm = TRUE)
  print(mediana_renda)
  dados$renda_media[is.na(dados$renda_media)] <- mediana_renda
  dados
}

converter_data_teste <- function(dados) {
  dados$data_teste <- as.Date(dados$data_teste)
  str(dados)
  dados
}

# --- Dados Categóricos ---

padronizar_genero <- function(dados) {
  print(summary(dados$genero))

  dados$genero[dados$genero %in% c("f", "F", "feminino")] <- "Feminino"
  dados$genero[dados$genero %in% c("m", "M", "masculino")] <- "Masculino"
  dados$genero[dados$genero %in% c("Não informado", "")] <- "Masculino"
  dados$genero <- factor(dados$genero)
  dados
}

padronizar_localidade <- function(dados) {
  dados$localidade[dados$localidade == ""] <- "Não Informado"
  dados
}

padronizar_nivel_educacional <- function(dados) {
  print(summary(dados$nivel_educacional))

  dados$nivel_educacional[dados$nivel_educacional %in% c("fundamnetal", "medio incompleto")] <- "Fundamental"
  dados$nivel_educacional[dados$nivel_educacional == "superio"] <- "Superior"
  dados$nivel_educacional[dados$nivel_educacional == ""] <- "Fundamental"
  dados$nivel_educacional <- factor(dados$nivel_educacional)
  dados
}

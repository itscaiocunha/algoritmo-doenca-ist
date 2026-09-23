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

# Substitui valores trabalhando sobre texto. Atribuir diretamente a um factor
# um rótulo que não está entre seus níveis gera NA em vez do valor desejado.
recodificar <- function(coluna, de, para) {
  valores <- as.character(coluna)
  valores[valores %in% de] <- para
  valores
}

# Gênero ausente vira uma categoria explícita: imputá-lo com a moda
# ("Masculino") inflaria artificialmente esse grupo.
padronizar_genero <- function(dados) {
  print(summary(dados$genero))

  dados$genero <- dados$genero |>
    recodificar(c("f", "F", "feminino"), "Feminino") |>
    recodificar(c("m", "M", "masculino"), "Masculino") |>
    recodificar(c("Não informado", ""), "Não Informado") |>
    factor()
  dados
}

padronizar_localidade <- function(dados) {
  dados$localidade <- dados$localidade |>
    recodificar("", "Não Informado") |>
    factor()
  dados
}

padronizar_nivel_educacional <- function(dados) {
  print(summary(dados$nivel_educacional))

  dados$nivel_educacional <- dados$nivel_educacional |>
    recodificar(c("fundamnetal", "medio incompleto"), "Fundamental") |>
    recodificar("superio", "Superior") |>
    recodificar("", "Fundamental") |>
    factor()
  dados
}

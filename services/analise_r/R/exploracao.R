# Análise exploratória: estatísticas descritivas, outliers e distribuições.

explorar_visao_geral <- function(dados) {
  print(head(dados))
  print(summary(dados))
  str(dados)
}

# Idade dos Pacientes
explorar_idade <- function(dados) {
  print(summary(dados$idade))
  boxplot(dados$idade, main = "Boxplot - Idade dos Pacientes",
          ylab = "Idades (em Anos)", col = "lightblue")
  hist(dados$idade)

  out_idade <- boxplot.stats(dados$idade)$out
  print(out_idade)  # Não existe discrepância nas Idades
}

# Renda Média dos Pacientes
explorar_renda <- function(dados) {
  print(summary(dados$renda_media))
  boxplot(dados$renda_media, main = "Boxplot - Renda Média dos Pacientes",
          ylab = "Valor em Reais (R$)", col = "red", outline = FALSE)

  out_renda <- boxplot.stats(dados$renda_media)$out
  print(length(out_renda))
  print(out_renda)
  print(dados[dados$renda_media %in% out_renda, ])
}

# Distribuição de uma variável categórica (tabela de frequência + gráfico de barras)
relatar_frequencias <- function(coluna, titulo, rotulo_x) {
  contagens <- table(coluna, dnn = NULL)
  print(contagens)
  barplot(contagens, main = titulo, xlab = rotulo_x)
}

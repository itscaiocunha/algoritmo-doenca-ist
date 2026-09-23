# Tratamento de Dados — orquestra a etapa de análise em R do pipeline:
# importação -> exploração -> tratamento -> exportação (CSV + PostgreSQL)

library(ggplot2)
library(dplyr)

source("R/config.R")
source("R/exploracao.R")
source("R/tratamento.R")
source("R/exportacao.R")

# --- Importação de Dados ---
dados <- read.csv(config$arquivo_entrada, sep = ",", stringsAsFactors = TRUE)

# --- Análise Exploratória ---
explorar_visao_geral(dados)
explorar_idade(dados)
explorar_renda(dados)

# --- Tratamento ---
dados <- dados |>
  imputar_renda_mediana() |>
  converter_data_teste() |>
  remover_datas_futuras() |>
  padronizar_genero() |>
  padronizar_localidade() |>
  padronizar_nivel_educacional()

relatar_frequencias(dados$genero, "Gênero", "Gênero")
relatar_frequencias(dados$doenca, "Doenças", "Doenças")
relatar_frequencias(dados$nivel_educacional, "Educação", "Nível de Estudo")

# --- Exportação ---
exportar_csv(dados, config$arquivo_saida)
exportar_postgres(dados, config$db)

FROM r-base:latest

# Dependências de sistema (compilação dos pacotes R e cliente do PostgreSQL para o pg_isready)
RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libpq-dev \
    postgresql-client \
    && apt-get clean

WORKDIR /app

# Pacotes R necessários
RUN R -e "install.packages(c('knitr', 'ggplot2', 'dplyr', 'tidyr', 'tools', 'RPostgreSQL'), repos='http://cran.r-project.org')"

COPY R/ ./R/
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]

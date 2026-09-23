# Imagem base com OpenJDK 8 (requisito do Spark 3.4)
FROM eclipse-temurin:8-jdk-focal

# Python 3.9, pip, bibliotecas BLAS/LAPACK e ferramentas de compilação
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3.9 python3.9-distutils python3-pip libatlas-base-dev gfortran build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

# Link do Java no caminho esperado pelo PySpark
RUN mkdir -p /usr/lib/jvm && \
    ln -s /opt/java/openjdk /usr/lib/jvm/java-8-openjdk-amd64

ENV JAVA_HOME="/opt/java/openjdk" \
    PYTHONPATH="/app"

WORKDIR /app
RUN mkdir -p /app/output /data

# O pip 20 do Ubuntu 20.04 não reconhece as wheels manylinux atuais e tenta
# compilar pacotes (ex.: pandas) do código-fonte; atualizá-lo evita a falha.
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt

COPY ist_bigdata/ ./ist_bigdata/
COPY main.ipynb .

# Executa o notebook e salva a versão com as saídas em /app/output
CMD ["jupyter", "nbconvert", "--to", "notebook", "--execute", "main.ipynb", "--output", "/app/output/resultado_main.ipynb", "--allow-errors"]

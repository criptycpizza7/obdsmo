FROM postgres:16

# установка дополнительных компонентов psql
RUN apt-get update && \
    apt-get install -y wget gnupg && \
    sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt bookworm-pgdg main" > /etc/apt/sources.list.d/pgdg.list' && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    apt-get update && \
    apt-get install -y build-essential git && \
    apt-get install -y postgresql-server-dev-16

# установка pgvector
RUN git clone https://github.com/pgvector/pgvector /tmp/pgvector && \
    cd /tmp/pgvector && \
    git checkout v0.7.0 && \
    echo "trusted = true" >> vector.control && \
    make && \
    make install && \
    rm -rf /tmp/pgvector

# запуск psql
CMD ["postgres"]

FROM biodepot/starbins:latest as builder

FROM debian:bookworm-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y gzip bzip2 \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /bin /usr/local/bin
COPY runstar.sh /usr/local/bin/runstar.sh
COPY version.sh /usr/local/bin/version.sh
ENV PATH="$PATH:/usr/local/bin" 
ENTRYPOINT ["version.sh"]
CMD ["runstar.sh"]
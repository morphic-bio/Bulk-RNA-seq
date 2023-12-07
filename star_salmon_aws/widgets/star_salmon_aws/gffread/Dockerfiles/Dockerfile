ARG samVersion=1.18
ARG gffreadVersion=0.12.7
ARG GCLIBversion=0.12.7
FROM debian:bookworm-slim as builder
ARG DEBIAN_FRONTEND=noninteractive
ARG samVersion
ARG gffreadVersion
ARG GCLIBversion

RUN apt-get update && apt-get -y install build-essential curl bzip2 zlib1g-dev 	libncurses-dev libbz2-dev liblzma-dev  libcurl4-openssl-dev
RUN curl -L https://github.com/samtools/samtools/releases/download/$samVersion/samtools-$samVersion.tar.bz2  | tar -jvxf - 
RUN curl -L https://github.com/gpertea/gffread/archive/refs/tags/v$gffreadVersion.tar.gz  | tar -zvxf - 
RUN curl -L https://github.com/gpertea/gclib/archive/refs/tags/v$GCLIBversion.tar.gz | tar -zvxf -
RUN mv gclib-$GCLIBversion gclib
WORKDIR samtools-$samVersion
RUN make -j 8
WORKDIR /gffread-$gffreadVersion
RUN make -j 8

FROM debian:bookworm-slim
ARG samVersion
ARG gffreadVersion
COPY --from=builder /samtools-$samVersion/samtools /usr/local/bin/samtools
COPY --from=builder /samtools-$samVersion/misc/ /usr/local/bin/
COPY --from=builder /lib/x86_64-linux-gnu/libcurl.so* /lib/x86_64-linux-gnu/
COPY --from=builder /lib/x86_64-linux-gnu/libncurses* /lib/x86_64-linux-gnu/
COPY --from=builder /lib/x86_64-linux-gnu/libnghttp2.so.14 /lib/x86_64-linux-gnu/
COPY --from=builder /lib/x86_64-linux-gnu/librtmp.so.1 /lib/x86_64-linux-gnu/
COPY --from=builder /lib/x86_64-linux-gnu/libssh* /lib/x86_64-linux-gnu/
COPY --from=builder /lib/x86_64-linux-gnu/libps* /lib/x86_64-linux-gnu/
COPY --from=builder /lib/x86_64-linux-gnu/libssl* /lib/x86_64-linux-gnu/
COPY --from=builder /lib/x86_64-linux-gnu/libcrypto* /lib/x86_64-linux-gnu/
COPY --from=builder /lib/x86_64-linux-gnu/libgssapi* /lib/x86_64-linux-gnu/
COPY --from=builder /lib/x86_64-linux-gnu/libldap* /lib/x86_64-linux-gnu/
COPY --from=builder /lib/x86_64-linux-gnu/liblber* /lib/x86_64-linux-gnu/
COPY --from=builder /lib/x86_64-linux-gnu/libbrotl* /lib/x86_64-linux-gnu/
COPY --from=builder /lib/x86_64-linux-gnu/libkrb5* /lib/x86_64-linux-gnu/
COPY --from=builder /lib/x86_64-linux-gnu/libk5crypto* /lib/x86_64-linux-gnu/
COPY --from=builder /lib/x86_64-linux-gnu/libsas* /lib/x86_64-linux-gnu/
COPY --from=builder /lib/x86_64-linux-gnu/libkeyutils* /lib/x86_64-linux-gnu/
COPY --from=builder /gffread-$gffreadVersion/gffread /usr/local/bin/gffread
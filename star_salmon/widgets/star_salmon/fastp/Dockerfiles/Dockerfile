ARG deflateVersion=1.18
ARG isalVersion=2.30.0
ARG fastpVersion=0.23.4
FROM debian:bookworm-slim as builder
ARG DEBIAN_FRONTEND=noninteractive
ARG deflateVersion
ARG isalVersion
ARG fastpVersion

RUN apt-get update && apt-get -y install build-essential curl autoconf automake libtool nasm yasm cmake
RUN curl -L https://github.com/intel/isa-l/archive/refs/tags/v${isalVersion}.tar.gz  | tar -zvxf - 
RUN curl -L https://github.com/ebiggers/libdeflate/archive/refs/tags/v${deflateVersion}.tar.gz | tar -zvxf - 
RUN curl -L https://github.com/OpenGene/fastp/archive/refs/tags/v${fastpVersion}.tar.gz | tar -zvxf - 

WORKDIR isa-l-${isalVersion}
RUN ./autogen.sh && ./configure --prefix=/usr --libdir=/usr/lib64 && make -j 8
RUN make install
WORKDIR /libdeflate-${deflateVersion}
RUN cmake -B build && cmake --build build && cmake --install build
WORKDIR /fastp-${fastpVersion}
RUN make -j8 && make install

FROM debian:bookworm-slim
COPY --from=builder /usr/local/bin/fastp /usr/local/bin/fastp
COPY --from=builder /usr/lib64 /usr/lib64/
COPY --from=builder /usr/lib/x86_64-linux-gnu/libdeflate.so.0 /usr/lib/x86_64-linux-gnu/libdeflate.so.0
ENV LD_LIBRARY_PATH=/usr/lib64
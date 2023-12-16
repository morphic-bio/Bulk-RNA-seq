FROM alpine:3.12.1
ADD samtools /source/samtools
RUN apk add --no-cache build-base zlib-dev bzip2-dev xz-dev ncurses-libs ncurses-dev curl-dev nano
RUN cd /source/samtools && make clean && make && make install
    

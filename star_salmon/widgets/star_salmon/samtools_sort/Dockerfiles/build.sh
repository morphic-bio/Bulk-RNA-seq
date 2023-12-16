 docker rmi alpine-bwa-sam-builder
 docker build -t "alpine-sam-builder" build
 mkdir -p usr/local/bin
 docker run --rm -v ${PWD}:/data alpine-sam-builder:latest /bin/sh -c 'cp /usr/local/bin/* /data/usr/local/bin/.'
 docker build -t biodepot/samtools:1.11__alpine_3.12.1 .
 docker rmi alpine-sam-builder:latest

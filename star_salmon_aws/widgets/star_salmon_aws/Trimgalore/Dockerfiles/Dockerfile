FROM debian:bullseye-slim
RUN apt-get update && apt-get -y install default-jre  libfindbin-libs-perl libhtsjdk-java libngs-java fastqc cutadapt curl isal\
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* 
 
RUN curl -L 'https://github.com/FelixKrueger/TrimGalore/archive/0.6.10.tar.gz' | tar -xzvf -
RUN ln -s /TrimGalore-0.6.10/trim_galore /usr/local/bin/trim_galore
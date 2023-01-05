FROM debian:bullseye

RUN apt update
RUN apt install -y build-essential wget git

WORKDIR /data

RUN mkdir texlive && \
  cd texlive && \
  wget https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz && \
  zcat install-tl-unx.tar.gz | tar xf - && \
  cd install-tl-* && \
  perl ./install-tl --no-interaction

ENV PATH="${PATH}:/usr/local/texlive/2022/bin/x86_64-linux"

RUN apt install -y ghostscript

RUN git clone https://gitlab.fi.muni.cz/external_relations/document_templates/fithesis.git
RUN cd fithesis && \
  make base && \
  make install-base to=/usr/share/texmf nohash=true && \
  texhash

WORKDIR /build

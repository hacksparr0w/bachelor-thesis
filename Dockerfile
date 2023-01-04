FROM miktex/miktex:latest

RUN apt update || true
RUN apt install -y git

WORKDIR /miktex/work
RUN GIT_SSL_NO_VERIFY=1 git clone https://gitlab.fi.muni.cz/external_relations/document_templates/fithesis.git
RUN cd fithesis && \
  make base && \
  make install-base to=/usr/share/texmf nohash=true && \
  initexmf -u --admin && \
  mpm --admin --update

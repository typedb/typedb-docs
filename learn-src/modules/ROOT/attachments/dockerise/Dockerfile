FROM ubuntu:22.04
WORKDIR /typedb-samples
EXPOSE 1729/tcp

COPY vaticle.gpg /etc/apt/trusted.gpg.d/vaticle.gpg
RUN echo "deb https://repo.typedb.com/public/public-release/deb/ubuntu trusty main" > /etc/apt/sources.list.d/vaticle.list
RUN apt update -y && apt install -y default-jre python3 python3-pip
RUN python3 -m pip install requests==2.31.0 pyyaml==6.0.1
COPY bootstrapper.py /typedb-samples

# We need the 'exec' before typedb server, or the SIGTERM from `docker stop` will not forwarded to it
CMD python3 -u bootstrapper.py; exec typedb server

FROM ubuntu:22.04
WORKDIR /typedb-samples
EXPOSE 1729/tcp

COPY typedb-samples-docker/vaticle.gpg /etc/apt/trusted.gpg.d/vaticle.gpg
RUN echo "deb https://repo.typedb.com/public/public-release/deb/ubuntu trusty main" > /etc/apt/sources.list.d/vaticle.list; apt update -y && apt install -y default-jre python3 python3-pip; python3 -m pip install requests==2.31.0 pyyaml==6.0.1
COPY typedb-samples-docker/bootstrapper.py /typedb-samples

# We need the 'exec' before typedb server, or the SIGTERM from `docker stop` will not forwarded to it
CMD python3 -u bootstrapper.py && exec typedb server


# The below copies are for testing. Uncomment if re-creating the master container.
COPY typedb-samples-docker/config.yml /typedb-samples/__test/config.yml
COPY learn-src/modules/ROOT/attachments/ /typedb-samples/__test

# To re-create the master container:
#   `docker build  . -f typedb-samples-docker/Dockerfile  --tag vaticle/typedb-sample-datasets:<VERSION>`

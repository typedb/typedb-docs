FROM ubuntu:22.04
WORKDIR /typedb-samples
COPY bootstrapper.py /typedb-samples
RUN apt update -y && apt install -y python3 python3-pip
RUN python3 -m pip install requests==2.31.0 pyyaml==6.0.1
CMD python3 bootstrapper.py

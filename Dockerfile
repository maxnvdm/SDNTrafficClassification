FROM ubuntu:trusty

# install required packages
WORKDIR /tests
COPY . /tests
RUN apt-get clean
RUN apt-get update \
    && apt-get install -y  git \
    net-tools \
    aptitude \
    build-essential \
    python-setuptools \
    python-dev \
    python-pip \
    software-properties-common \
    curl \
    iptables \
    iputils-ping \
    wget \
    firefox \
    tcpdump \
    ubuntu-restricted-extras
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.25.0/geckodriver-v0.25.0-linux64.tar.gz
RUN tar -xvzf geckodriver-v0.25.0-linux64.tar.gz
RUN chmod +x geckodriver
RUN mv geckodriver /usr/bin/
RUN pip install selenium
RUN pip install --upgrade --ignore-installed urllib3



#CMD ["python", "/tests/vulatest.py"]

# docker run --name tests -it -v /home/max/Documents/tests/:/tests/ /bin/bash

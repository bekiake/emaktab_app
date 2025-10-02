FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git zip unzip openjdk-8-jdk python3-pip autoconf libtool \
    pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev \
    libtinfo5 cmake libffi-dev libssl-dev \
    build-essential python3-dev ccache ant wget curl

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install buildozer cython

# Set up working directory
WORKDIR /app

# Set Java environment
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

# Copy app files
COPY . /app

# Install app requirements
RUN pip3 install -r requirements.txt

# Build command
CMD ["buildozer", "android", "debug"]
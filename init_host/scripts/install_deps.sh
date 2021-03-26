#!/bin/bash

sudo apt-get install python2 python2-dev python3 python3-dev python3-pip python3-psutil python3-yaml -y
sudo python2 get-pip.py

sudo pip2 install -i https://pypi.tuna.tsinghua.edu.cn/simple psutil paramiko lockfile setuptools

sudo apt-get update -y
sudo apt-get install -y \
  bison \
  ccache \
  cmake \
  curl \
  flex \
  git-core \
  gcc \
  g++ \
  inetutils-ping \
  libapr1-dev \
  libbz2-dev \
  libcurl4-gnutls-dev \
  libevent-dev \
  libpam-dev \
  libperl-dev \
  libreadline-dev \
  libssl-dev \
  libxml2-dev \
  libyaml-dev \
  libzstd-dev \
  locales \
  net-tools \
  ninja-build \
  openssh-client \
  openssh-server \
  openssl \
  zlib1g-dev \
  pkg-config

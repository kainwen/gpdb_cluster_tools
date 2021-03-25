## Host Init

[https://gpdb.docs.pivotal.io/6-15/install\_guide/prep\_os.html](https://gpdb.docs.pivotal.io/6-15/install\_guide/prep\_os.html)

1. use `ssh-copy-id` to set ssh without password
2. use `visudo` to gpadmin
3. Each host generate ssh-key: `ssh-keygen`
4. disk io read-ahead, change root's crontab: `@reboot  /sbin/blockdev --setra 16384 /dev/???`
5. Disable Transparent Huge Pages: ` sudo apt install libhugetlbfs-bin; sudo hugeadm --thp-never`
6. XFS mount parameter: `rw,nodev,noatime,inode64`, like `/dev/data /data xfs nodev,noatime,nobarrier,inode64 0 0`
7. set rlimit
8. set sysctl
9. Reboot

## Dependency

### Compile xerces

https://github.com/greenplum-db/gp-xerces.git

### Python2 and Python3

```
sudo apt-get install python2 python2-dev python3 python3-dev python3-pip python3-psutil python3-yaml -y
sudo python2 get-pip.py

sudo pip2 install -i https://pypi.tuna.tsinghua.edu.cn/simple psutil paramiko lockfile setuptools
```

Use `set_python.sh` to set python.

### Deps

```
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
```

### Compile source code

### Install pygresql

## Tune GUCs